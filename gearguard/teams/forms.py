from django import forms
from .models import Team

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'company', 'description', 'work_center']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2',
                'placeholder': 'Team name'
            }),
            'company': forms.TextInput(attrs={
                'class': 'w-full bg-slate-900 border border-slate-700 text-white rounded-md p-3 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors',
                'placeholder': 'Company Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2',
                'rows': 3,
                'placeholder': 'Team description'
            }),
            'work_center': forms.Select(attrs={
                'class': 'w-full bg-slate-900 border-slate-800 text-white rounded p-2'
            }),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name.strip()) == 0:
            raise forms.ValidationError('Team name cannot be empty.')
        return name
