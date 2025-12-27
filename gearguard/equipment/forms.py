from django import forms
from .models import Equipment

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = [
            'name', 'company', 'category', 'serial_number', 'description',
            'employee', 'maintenance_team', 'work_center',
            'assigned_date', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-md p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors',
                'placeholder': 'Equipment Name'
            }),
            'company': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-md p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors',
                'placeholder': 'Company Name'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-md p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors'
            }),
            'serial_number': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-md p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors',
                'placeholder': 'Serial Number'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-md p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors',
                'rows': 4,
                'placeholder': 'Equipment Description'
            }),
            'employee': forms.Select(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-md p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors'
            }),
            'maintenance_team': forms.Select(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-md p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors'
            }),
            'work_center': forms.Select(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-md p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors'
            }),
            'assigned_date': forms.DateInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-md p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-md p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors'
            }),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name.strip()) == 0:
            raise forms.ValidationError('Equipment name cannot be empty.')
        return name
