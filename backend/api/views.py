from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Count
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from datetime import datetime

from .models import Dataset, EquipmentRecord
from .serializers import (
    UserSerializer, 
    DatasetSerializer, 
    DatasetSummarySerializer,
    EquipmentRecordSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user and return JWT tokens"""
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Try to authenticate with email first, then username
    user = None
    if email:
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            pass
    elif username:
        user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get current user profile"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """Upload and process CSV file"""
    if 'file' not in request.FILES:
        return Response(
            {'error': 'No file provided'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    csv_file = request.FILES['file']
    
    # Validate file extension
    if not csv_file.name.endswith('.csv'):
        return Response(
            {'error': 'File must be a CSV'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Read CSV with pandas
        df = pd.read_csv(csv_file)
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        if not all(col in df.columns for col in required_columns):
            return Response(
                {'error': f'CSV must contain columns: {", ".join(required_columns)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate statistics
        total_count = len(df)
        avg_flowrate = df['Flowrate'].mean()
        avg_pressure = df['Pressure'].mean()
        avg_temperature = df['Temperature'].mean()
        
        # Equipment type distribution
        equipment_types = df['Type'].value_counts().to_dict()
        
        # Create dataset
        dataset = Dataset.objects.create(
            user=request.user,
            filename=csv_file.name,
            total_count=total_count,
            avg_flowrate=round(avg_flowrate, 2),
            avg_pressure=round(avg_pressure, 2),
            avg_temperature=round(avg_temperature, 2),
            equipment_types=equipment_types
        )
        
        # Create equipment records
        records = []
        for _, row in df.iterrows():
            records.append(EquipmentRecord(
                dataset=dataset,
                equipment_name=row['Equipment Name'],
                equipment_type=row['Type'],
                flowrate=row['Flowrate'],
                pressure=row['Pressure'],
                temperature=row['Temperature']
            ))
        
        EquipmentRecord.objects.bulk_create(records)
        
        # Keep only last 5 datasets per user
        user_datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
        if user_datasets.count() > 5:
            datasets_to_delete = user_datasets[5:]
            Dataset.objects.filter(id__in=[d.id for d in datasets_to_delete]).delete()
        
        # Return dataset with records
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Error processing file: {str(e)}'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_datasets(request):
    """Get all datasets for current user"""
    datasets = Dataset.objects.filter(user=request.user)
    serializer = DatasetSummarySerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset_detail(request, dataset_id):
    """Get detailed dataset with all records"""
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dataset(request, dataset_id):
    """Delete a dataset"""
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        dataset.delete()
        return Response(
            {'message': 'Dataset deleted successfully'}, 
            status=status.HTTP_200_OK
        )
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf_report(request, dataset_id):
    """Generate PDF report for a dataset"""
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        records = dataset.records.all()
        
        # Create PDF buffer
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
        )
        
        # Title
        title = Paragraph("Chemical Equipment Analysis Report", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Dataset Info
        info_data = [
            ['Filename:', dataset.filename],
            ['Upload Date:', dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')],
            ['Total Equipment:', str(dataset.total_count)],
            ['User:', dataset.user.username],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary Statistics
        elements.append(Paragraph("Summary Statistics", heading_style))
        summary_data = [
            ['Metric', 'Value'],
            ['Average Flowrate', f"{dataset.avg_flowrate:.2f}"],
            ['Average Pressure', f"{dataset.avg_pressure:.2f}"],
            ['Average Temperature', f"{dataset.avg_temperature:.2f}"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Equipment Type Distribution
        elements.append(Paragraph("Equipment Type Distribution", heading_style))
        type_data = [['Equipment Type', 'Count']]
        for eq_type, count in dataset.equipment_types.items():
            type_data.append([eq_type, str(count)])
        
        type_table = Table(type_data, colWidths=[3*inch, 3*inch])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
        ]))
        elements.append(type_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Equipment Records
        elements.append(PageBreak())
        elements.append(Paragraph("Detailed Equipment Records", heading_style))
        
        record_data = [['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
        for record in records:
            record_data.append([
                record.equipment_name,
                record.equipment_type,
                f"{record.flowrate:.1f}",
                f"{record.pressure:.1f}",
                f"{record.temperature:.1f}"
            ])
        
        record_table = Table(record_data, colWidths=[2*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
        record_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
        ]))
        elements.append(record_table)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        # Return response
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{dataset.filename}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
        return response
        
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
