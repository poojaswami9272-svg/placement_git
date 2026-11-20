from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('STUDENT', 'Student'),
        ('OFFICER', 'Placement Officer'),
        ('ADMIN', 'Administrator'),
    )
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='STUDENT')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    @property
    def is_student(self):
        return self.user_type == 'STUDENT'

    @property
    def is_officer(self):
        return self.user_type in ['OFFICER', 'ADMIN'] or self.is_staff or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
