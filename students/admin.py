from django.contrib import admin
from .models import StudentProfile, StudentSkill, StudentProject, StudentCertification, StudentDocument

class StudentSkillInline(admin.TabularInline):
    model = StudentSkill
    extra = 1

class StudentProjectInline(admin.TabularInline):
    model = StudentProject
    extra = 1

class StudentCertificationInline(admin.TabularInline):
    model = StudentCertification
    extra = 1

class StudentDocumentInline(admin.TabularInline):
    model = StudentDocument
    extra = 1

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'full_name', 'department', 'current_year', 'cgpa', 'active_backlogs', 'placement_status', 'resume_status')
    list_filter = ('department', 'current_year', 'placement_status', 'resume_status')
    search_fields = ('full_name', 'roll_number', 'skills', 'user__email')
    inlines = [StudentSkillInline, StudentProjectInline, StudentCertificationInline, StudentDocumentInline]

@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ('student', 'doc_type', 'uploaded_at')
    list_filter = ('doc_type',)
