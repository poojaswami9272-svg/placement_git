from django.db import models
from django.conf import settings

NOTIFICATION_TYPE_CHOICES = (
    ('DRIVE', 'Placement Drive'),
    ('APPLICATION', 'Application Status'),
    ('INTERVIEW', 'Interview Scheduled'),
    ('SELECTION', 'Selection Announcement'),
    ('ANNOUNCEMENT', 'Campus Notice'),
    ('SYSTEM', 'System Alert'),
)

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=25, choices=NOTIFICATION_TYPE_CHOICES, default='SYSTEM')
    link_url = models.CharField(max_length=255, blank=True, default='/dashboard/')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"

    @property
    def icon_class(self):
        icons = {
            'DRIVE': 'fa-solid fa-briefcase',
            'APPLICATION': 'fa-solid fa-file-lines',
            'INTERVIEW': 'fa-solid fa-calendar-check',
            'SELECTION': 'fa-solid fa-award',
            'ANNOUNCEMENT': 'fa-solid fa-bullhorn',
            'SYSTEM': 'fa-solid fa-bell',
        }
        return icons.get(self.notification_type, 'fa-solid fa-bell')
