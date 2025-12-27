from django.db import models
from django.contrib.auth.models import User

class MaintenanceRequest(models.Model):
    MAINTENANCE_FOR_CHOICES = [
        ('equipment', 'Equipment'),
        ('work_center', 'Work Center'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    
    TYPE_CHOICES = [
        ('corrective', 'Corrective'),
        ('preventive', 'Preventive'),
    ]
    
    STAGE_CHOICES = [
        ('new', 'New Request'),
        ('in_progress', 'In Progress'),
        ('repaired', 'Repaired'),
        ('scrapped', 'Scrapped'),
    ]

    subject = models.CharField(max_length=200)
    maintenance_for = models.CharField(max_length=20, choices=MAINTENANCE_FOR_CHOICES, default='equipment')
    
    # Selection based on maintenance_for
    equipment = models.ForeignKey('equipment.Equipment', null=True, blank=True, on_delete=models.SET_NULL)
    work_center = models.ForeignKey('teams.WorkCenter', null=True, blank=True, on_delete=models.SET_NULL)
    
    # Details
    created_by = models.ForeignKey(User, related_name='created_requests', on_delete=models.SET_NULL, null=True)
    technician = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey('teams.Team', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Scheduling
    request_date = models.DateField(auto_now_add=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    
    # Categorization
    maintenance_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='corrective')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='new')
    
    notes = models.TextField(blank=True)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return self.subject
