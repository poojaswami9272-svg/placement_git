from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name', 'logo', 'description', 'industry', 'company_type',
            'website', 'location', 'contact_email', 'contact_phone',
            'hr_name', 'average_package', 'highest_package', 'is_featured'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Google India'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Overview of the enterprise, work culture, hiring practices...'}),
            'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Software, Cloud & AI, IT Services'}),
            'company_type': forms.Select(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bangalore, Hyderabad, Pune'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'recruitment@company.com'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 ...'}),
            'hr_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'University Hiring Lead'}),
            'average_package': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'e.g. 7.5'}),
            'highest_package': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'e.g. 18.0'}),
            'is_featured': forms.CheckboxInput(attrs={'style': 'margin-left: 8px;'}),
        }
