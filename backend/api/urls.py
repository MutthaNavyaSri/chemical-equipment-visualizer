from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/profile/', views.get_user_profile, name='profile'),
    
    # Dataset operations
    path('datasets/', views.get_datasets, name='datasets'),
    path('datasets/upload/', views.upload_csv, name='upload_csv'),
    path('datasets/<int:dataset_id>/', views.get_dataset_detail, name='dataset_detail'),
    path('datasets/<int:dataset_id>/delete/', views.delete_dataset, name='delete_dataset'),
    path('datasets/<int:dataset_id>/report/', views.generate_pdf_report, name='generate_report'),
]
