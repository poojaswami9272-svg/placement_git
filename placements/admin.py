from django.contrib import admin
from .models import PlacementDrive, Announcement

@admin.register(PlacementDrive)
class PlacementDriveAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'salary_package', 'minimum_cgpa', 'application_deadline', 'drive_date', 'is_active')
    list_filter = ('job_type', 'is_active', 'drive_date', 'company')
    search_fields = ('title', 'company__name', 'required_skills', 'description')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_pinned', 'created_at')
    list_filter = ('category', 'is_pinned')
    search_fields = ('title', 'content')
