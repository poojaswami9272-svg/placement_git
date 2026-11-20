from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from students.models import StudentProfile, DEPARTMENT_CHOICES, YEAR_CHOICES

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. rahul_sharma'}))
    first_name = forms.CharField(max_length=150, label="First Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=150, label="Last Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'student@college.edu'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 9876543210'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create strong password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))

    # Student Profile Fields
    roll_number = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 21CS045'}))
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    current_year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    cgpa = forms.DecimalField(max_digits=4, decimal_places=2, min_value=0.0, max_value=10.0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 8.45'}))
    skills = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Django, SQL, JavaScript'}))
    career_interests = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Software Engineer, Backend Developer, Data Analyst'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        confirm_pwd = cleaned_data.get('confirm_password')

        if pwd and confirm_pwd and pwd != confirm_pwd:
            self.add_error('confirm_password', "Passwords do not match.")

        roll = cleaned_data.get('roll_number')
        if roll and StudentProfile.objects.filter(roll_number__iexact=roll).exists():
            self.add_error('roll_number', "A student profile with this Roll Number already exists.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.user_type = 'STUDENT'
        if commit:
            user.save()
            full_name = f"{self.cleaned_data.get('first_name')} {self.cleaned_data.get('last_name')}".strip()
            StudentProfile.objects.create(
                user=user,
                roll_number=self.cleaned_data.get('roll_number'),
                full_name=full_name or user.username,
                department=self.cleaned_data.get('department'),
                current_year=self.cleaned_data.get('current_year'),
                cgpa=self.cleaned_data.get('cgpa'),
                skills=self.cleaned_data.get('skills'),
                career_interests=self.cleaned_data.get('career_interests') or 'Software Development',
            )
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
