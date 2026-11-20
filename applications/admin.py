from django.contrib import admin
from .models import JobApplication, InterviewSchedule, PlacementOffer

class InterviewScheduleInline(admin.TabularInline):
    model = InterviewSchedule
    extra = 0

class PlacementOfferInline(admin.StackedInline):
    model = PlacementOffer
    extra = 0

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'status', 'applied_date', 'updated_at')
    list_filter = ('status', 'applied_date', 'job__company')
    search_fields = ('student__full_name', 'student__roll_number', 'job__title', 'job__company__name')
    inlines = [InterviewScheduleInline, PlacementOfferInline]

@admin.register(InterviewSchedule)
class InterviewScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'application', 'interview_type', 'interview_date', 'interview_time', 'interview_status')
    list_filter = ('interview_type', 'interview_status', 'interview_date')

@admin.register(PlacementOffer)
class PlacementOfferAdmin(admin.ModelAdmin):
    list_display = ('application', 'job_role', 'package_offered', 'selection_date', 'is_accepted')
    list_filter = ('selection_date', 'is_accepted')
