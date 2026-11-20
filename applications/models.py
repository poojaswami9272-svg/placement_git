from django.db import models
from students.models import StudentProfile
from placements.models import PlacementDrive

APPLICATION_STATUS_CHOICES = (
    ('APPLIED', 'Applied'),
    ('SHORTLISTED', 'Shortlisted'),
    ('APTITUDE_TEST', 'Aptitude Test'),
    ('TECHNICAL_INTERVIEW', 'Technical Interview'),
    ('HR_INTERVIEW', 'HR Interview'),
    ('SELECTED', 'Selected'),
    ('REJECTED', 'Rejected'),
)

INTERVIEW_TYPE_CHOICES = (
    ('APTITUDE_TEST', 'Aptitude Test'),
    ('CODING_TEST', 'Coding Assessment'),
    ('TECHNICAL_INTERVIEW', 'Technical Interview'),
    ('HR_INTERVIEW', 'HR Interview'),
    ('GROUP_DISCUSSION', 'Group Discussion'),
)

INTERVIEW_STATUS_CHOICES = (
    ('SCHEDULED', 'Scheduled'),
    ('COMPLETED', 'Completed'),
    ('CANCELLED', 'Cancelled'),
    ('RESCHEDULED', 'Rescheduled'),
)

class JobApplication(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(PlacementDrive, on_delete=models.CASCADE, related_name='applications')
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=APPLICATION_STATUS_CHOICES, default='APPLIED')
    resume_file = models.FileField(upload_to='resumes_submitted/', blank=True, null=True)
    notes = models.TextField(blank=True, default='')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'job')
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.student.full_name} -> {self.job.title} ({self.get_status_display()})"

    @property
    def status_badge_class(self):
        badge_map = {
            'APPLIED': 'badge-primary',
            'SHORTLISTED': 'badge-purple',
            'APTITUDE_TEST': 'badge-warning',
            'TECHNICAL_INTERVIEW': 'badge-orange',
            'HR_INTERVIEW': 'badge-info',
            'SELECTED': 'badge-success',
            'REJECTED': 'badge-danger',
        }
        return badge_map.get(self.status, 'badge-secondary')


class InterviewSchedule(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='interviews')
    title = models.CharField(max_length=150, default="Interview Round")
    interview_type = models.CharField(max_length=30, choices=INTERVIEW_TYPE_CHOICES, default='TECHNICAL_INTERVIEW')
    interview_date = models.DateField()
    interview_time = models.TimeField()
    location_or_link = models.CharField(max_length=255, default='Campus Placement Cell, Block-A')
    interview_status = models.CharField(max_length=20, choices=INTERVIEW_STATUS_CHOICES, default='SCHEDULED')
    interviewer_notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['interview_date', 'interview_time']

    def __str__(self):
        return f"{self.get_interview_type_display()} for {self.application.student.full_name} ({self.interview_date})"


class PlacementOffer(models.Model):
    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE, related_name='offer')
    package_offered = models.DecimalField(max_digits=5, decimal_places=2, help_text="In LPA")
    job_role = models.CharField(max_length=150)
    selection_date = models.DateField()
    offer_letter = models.FileField(upload_to='offers/', blank=True, null=True)
    is_accepted = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer: {self.job_role} at {self.application.job.company.name} ({self.package_offered} LPA)"
