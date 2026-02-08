from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Dataset(models.Model):
    """Model to store uploaded CSV datasets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)
    total_count = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    equipment_types = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class EquipmentRecord(models.Model):
    """Model to store individual equipment records"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='records')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"
