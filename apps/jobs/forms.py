from django import forms
from .models import Job

class JobCreateForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'requirements', 
            'location', 'job_type', 'salary',
            'application_deadline'
        ]
        widgets = {
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
        }

class JobUpdateForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'requirements',
            'location', 'job_type', 'salary',
            'application_deadline', 'is_active'
        ]