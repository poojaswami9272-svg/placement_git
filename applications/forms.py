from django import forms
from .models import JobApplication, InterviewSchedule, PlacementOffer

class ApplicationStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Internal officer notes or reason for status update...'}),
        }


class InterviewScheduleForm(forms.ModelForm):
    class Meta:
        model = InterviewSchedule
        fields = ['title', 'interview_type', 'interview_date', 'interview_time', 'location_or_link', 'interviewer_notes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Round 1 Technical Coding'}),
            'interview_type': forms.Select(attrs={'class': 'form-control'}),
            'interview_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'interview_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location_or_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Placement Cell Lab 2 or Google Meet Link'}),
            'interviewer_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Instructions for the candidate...'}),
        }


class PlacementOfferForm(forms.ModelForm):
    class Meta:
        model = PlacementOffer
        fields = ['job_role', 'package_offered', 'selection_date', 'offer_letter']
        widgets = {
            'job_role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Associate Software Engineer'}),
            'package_offered': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'e.g. 9.5'}),
            'selection_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'offer_letter': forms.FileInput(attrs={'class': 'form-control'}),
        }
