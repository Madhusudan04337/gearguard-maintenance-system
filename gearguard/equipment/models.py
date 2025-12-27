from django.db import models
from django.contrib.auth.models import User

class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = "Equipment Categories"

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    serial_number = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    
    # Relationships from workflow
    employee = models.ForeignKey(User, related_name='used_equipment', on_delete=models.SET_NULL, null=True, blank=True)
    maintenance_team = models.ForeignKey('teams.Team', on_delete=models.SET_NULL, null=True, blank=True)
    work_center = models.ForeignKey('teams.WorkCenter', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Dates
    assigned_date = models.DateField(null=True, blank=True)
    scrap_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('under_maintenance', 'Under Maintenance'),
        ('scrapped', 'Scrapped'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name
