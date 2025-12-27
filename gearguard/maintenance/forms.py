from django.db import models
from django import forms
from .models import MaintenanceRequest
from datetime import datetime, timedelta
import re

class MaintenanceRequestForm(forms.ModelForm):
    duration_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2',
            'placeholder': 'HH:MM:SS (e.g., 02:30:45)'
        }),
        help_text='Format: HH:MM:SS'
    )
    
    class Meta:
        model = MaintenanceRequest
        fields = [
            'subject', 'maintenance_for', 'equipment', 'work_center', 
            'technician', 'team', 'scheduled_date', 
            'maintenance_type', 'priority', 'notes', 'instructions'
        ]
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'maintenance_for': forms.Select(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'equipment': forms.Select(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'work_center': forms.Select(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'technician': forms.Select(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'team': forms.Select(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'scheduled_date': forms.DateTimeInput(attrs={
                'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2',
                'type': 'datetime-local'
            }),
            'maintenance_type': forms.RadioSelect(attrs={'class': 'flex gap-4'}),
            'priority': forms.Select(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'}),
            'notes': forms.Textarea(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2', 'rows': 3}),
            'instructions': forms.Textarea(attrs={'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2', 'rows': 3}),
        }
    
    def clean_scheduled_date(self):
        scheduled_date = self.cleaned_data.get('scheduled_date')
        if scheduled_date and scheduled_date < datetime.now():
            raise forms.ValidationError('Scheduled date must be in the future.')
        return scheduled_date
    
    def clean_duration_input(self):
        duration_input = self.cleaned_data.get('duration_input')
        if duration_input:
            # Validate HH:MM:SS format
            pattern = r'^(\d{1,2}):(\d{2}):(\d{2})$'
            if not re.match(pattern, duration_input):
                raise forms.ValidationError(
                    'Duration must be in HH:MM:SS format (e.g., 02:30:45).'
                )
            
            # Parse and validate time components
            try:
                parts = duration_input.split(':')
                hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
                
                if minutes >= 60 or seconds >= 60:
                    raise forms.ValidationError(
                        'Minutes and seconds must be less than 60.'
                    )
                
                if hours > 999:  # Reasonable upper limit
                    raise forms.ValidationError(
                        'Hours cannot exceed 999.'
                    )
            except (ValueError, IndexError):
                raise forms.ValidationError(
                    'Invalid duration format. Use HH:MM:SS.'
                )
        return duration_input
    
    def clean(self):
        cleaned_data = super().clean()
        duration_input = cleaned_data.get('duration_input')
        
        if duration_input:
            try:
                parts = duration_input.split(':')
                hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
                cleaned_data['duration'] = timedelta(
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds
                )
            except (ValueError, AttributeError):
                pass
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Set duration from duration_input if provided
        duration_input = self.cleaned_data.get('duration_input')
        if duration_input:
            parts = duration_input.split(':')
            instance.duration = timedelta(
                hours=int(parts[0]),
                minutes=int(parts[1]),
                seconds=int(parts[2])
            )
        if commit:
            instance.save()
        return instance
