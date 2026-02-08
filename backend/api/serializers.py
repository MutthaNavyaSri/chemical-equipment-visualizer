from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dataset, EquipmentRecord


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class EquipmentRecordSerializer(serializers.ModelSerializer):
    """Serializer for Equipment Record model"""
    
    class Meta:
        model = EquipmentRecord
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class DatasetSerializer(serializers.ModelSerializer):
    """Serializer for Dataset model"""
    records = EquipmentRecordSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'uploaded_at', 'username',
            'total_count', 'avg_flowrate', 'avg_pressure', 
            'avg_temperature', 'equipment_types', 'records'
        ]
        read_only_fields = ['uploaded_at']


class DatasetSummarySerializer(serializers.ModelSerializer):
    """Serializer for Dataset summary (without records)"""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'uploaded_at', 'username',
            'total_count', 'avg_flowrate', 'avg_pressure', 
            'avg_temperature', 'equipment_types'
        ]
