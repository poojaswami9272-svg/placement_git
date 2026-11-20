from django.db import models
from django.conf import settings

class ResumeAnalysisLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resume_analyses')
    target_role = models.CharField(max_length=150, default='Software Engineer')
    score = models.IntegerField(default=75)
    skills_found = models.TextField(blank=True, default='')
    missing_skills = models.TextField(blank=True, default='')
    recommendations = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.target_role} ({self.score}/100)"


class AIChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_chats')
    role = models.CharField(max_length=15, choices=(('user', 'User'), ('assistant', 'AI Assistant')))
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"[{self.role}] {self.user.username}: {self.message[:40]}"
