from django.db import models
from django.conf import settings

DEPARTMENT_CHOICES = (
    ('CSE', 'Computer Science & Engineering'),
    ('IT', 'Information Technology'),
    ('AI_DS', 'AI & Data Science'),
    ('ECE', 'Electronics & Communication'),
    ('EEE', 'Electrical & Electronics'),
    ('MECH', 'Mechanical Engineering'),
    ('CIVIL', 'Civil Engineering'),
    ('MCA', 'Master of Computer Applications'),
    ('MBA', 'Master of Business Administration'),
)

YEAR_CHOICES = (
    (1, '1st Year'),
    (2, '2nd Year'),
    (3, '3rd Year'),
    (4, '4th Year / Final Year'),
)

PLACEMENT_STATUS_CHOICES = (
    ('NOT_PLACED', 'Not Placed'),
    ('APPLIED', 'Applied'),
    ('SHORTLISTED', 'Shortlisted'),
    ('INTERVIEWING', 'Interviewing'),
    ('SELECTED', 'Selected'),
    ('PLACED', 'Placed'),
)

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=120)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='CSE')
    current_year = models.IntegerField(choices=YEAR_CHOICES, default=4)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=7.50)
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=85.0)
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=85.0)
    active_backlogs = models.IntegerField(default=0)
    skills = models.TextField(blank=True, default='Python, Django, SQL, JavaScript')
    career_interests = models.TextField(blank=True, default='Software Development, Web Development, Data Science')
    placement_status = models.CharField(max_length=20, choices=PLACEMENT_STATUS_CHOICES, default='NOT_PLACED')
    profile_photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    resume_status = models.CharField(max_length=20, default='Missing', choices=(
        ('Missing', 'Missing'),
        ('Uploaded', 'Uploaded'),
        ('Updated', 'Updated'),
    ))
    bio = models.TextField(blank=True, default='Aspiring engineer eager to build impactful software solutions.')
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.roll_number}) - {self.department}"

    @property
    def skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    @property
    def completion_percentage(self):
        """Calculates dynamic profile completion percentage."""
        fields_to_check = [
            self.full_name,
            self.roll_number,
            self.department,
            self.current_year,
            self.cgpa,
            self.tenth_percentage,
            self.twelfth_percentage,
            self.skills,
            self.career_interests,
            self.profile_photo,
            self.resume_file,
            self.bio,
            self.linkedin_url or self.github_url,
        ]
        filled = sum(1 for f in fields_to_check if f)
        total = len(fields_to_check)
        return int((filled / total) * 100)


class StudentSkill(models.Model):
    PROFICIENCY_CHOICES = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert'),
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='detailed_skills')
    skill_name = models.CharField(max_length=80)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='Intermediate')

    def __str__(self):
        return f"{self.skill_name} ({self.proficiency})"


class StudentProject(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200, help_text="e.g. Django, React, SQLite")
    project_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class StudentCertification(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=150)
    issue_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.issuing_organization}"


class StudentDocument(models.Model):
    DOC_TYPES = (
        ('Resume', 'Resume'),
        ('10th_Marksheet', '10th Marksheet'),
        ('12th_Marksheet', '12th Marksheet'),
        ('College_ID', 'College ID Proof'),
        ('Certificate', 'Achievement Certificate'),
        ('Other', 'Other Document'),
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=30, choices=DOC_TYPES, default='Other')
    document_file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_doc_type_display()} - {self.student.full_name}"
