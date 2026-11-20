from django import forms
from .models import PlacementDrive, Announcement
from companies.models import Company

class PlacementDriveForm(forms.ModelForm):
    class Meta:
        model = PlacementDrive
        fields = [
            'company', 'title', 'job_type', 'experience_required', 'description', 'location',
            'salary_package', 'minimum_cgpa', 'max_backlogs',
            'eligible_departments', 'eligible_years', 'required_skills',
            'vacancies', 'application_deadline', 'drive_date',
            'selection_process', 'banner_image', 'is_active'
        ]
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Associate Software Engineer'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'experience_required': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Job responsibilities and qualifications...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bangalore / Remote / Hybrid'}),
            'salary_package': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'e.g. 10.5'}),
            'minimum_cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'e.g. 7.0'}),
            'max_backlogs': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 0'}),
            'eligible_departments': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CSE,IT,AI_DS,ECE,EEE'}),
            'eligible_years': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '3,4'}),
            'required_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, SQL, Git, REST API'}),
            'vacancies': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 15'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'drive_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'selection_process': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'banner_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'style': 'margin-left: 8px;'}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'category', 'content', 'related_job', 'is_pinned']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Announcement title...'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed announcement content...'}),
            'related_job': forms.Select(attrs={'class': 'form-control'}),
            'is_pinned': forms.CheckboxInput(attrs={'style': 'margin-left: 8px;'}),
        }
