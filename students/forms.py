from django import forms
from .models import StudentProfile, StudentSkill, StudentProject, StudentCertification, StudentDocument

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'full_name', 'department', 'current_year', 'cgpa', 
            'tenth_percentage', 'twelfth_percentage', 'active_backlogs',
            'skills', 'career_interests', 'bio', 'profile_photo',
            'linkedin_url', 'github_url', 'portfolio_url'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'current_year': forms.Select(attrs={'class': 'form-control'}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tenth_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'twelfth_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'active_backlogs': forms.NumberInput(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control'}),
            'career_interests': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['resume_file']
        widgets = {
            'resume_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
        }


class StudentProjectForm(forms.ModelForm):
    class Meta:
        model = StudentProject
        fields = ['title', 'technologies', 'description', 'project_url', 'github_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'technologies': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'project_url': forms.URLInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class StudentCertificationForm(forms.ModelForm):
    class Meta:
        model = StudentCertification
        fields = ['title', 'issuing_organization', 'issue_date', 'credential_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'credential_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class StudentDocumentForm(forms.ModelForm):
    class Meta:
        model = StudentDocument
        fields = ['doc_type', 'document_file']
        widgets = {
            'doc_type': forms.Select(attrs={'class': 'form-control'}),
            'document_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
