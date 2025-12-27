from django.db import models
from django import forms
from .models import MaintenanceRequest

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = [
            'subject', 'maintenance_for', 'equipment', 'work_center', 
            'technician', 'team', 'scheduled_date', 'duration', 
            'maintenance_type', 'priority', 'notes', 'instructions'
        ]
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'maintenance_for': forms.Select(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'equipment': forms.Select(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'work_center': forms.Select(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'technician': forms.Select(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'team': forms.Select(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'scheduled_date': forms.DateTimeInput(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2', 'type': 'datetime-local'}),
            'duration': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2', 'placeholder': 'HH:MM:SS'}),
            'maintenance_type': forms.RadioSelect(attrs={'class': 'flex gap-4'}),
            'priority': forms.Select(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'notes': forms.Textarea(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2', 'rows': 3}),
            'instructions': forms.Textarea(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2', 'rows': 3}),
        }
