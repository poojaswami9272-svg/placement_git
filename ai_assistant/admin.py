from django.contrib import admin
from .models import ResumeAnalysisLog, AIChatMessage

@admin.register(ResumeAnalysisLog)
class ResumeAnalysisLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_role', 'score', 'created_at')
    list_filter = ('target_role', 'created_at')

@admin.register(AIChatMessage)
class AIChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'timestamp')
    list_filter = ('role', 'timestamp')
