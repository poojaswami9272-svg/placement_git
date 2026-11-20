from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, FileResponse, Http404
from .models import StudentProfile, StudentSkill, StudentProject, StudentCertification, StudentDocument
from .forms import (
    StudentProfileForm, ResumeUploadForm, StudentProjectForm, 
    StudentCertificationForm, StudentDocumentForm
)
from notifications.models import Notification

@login_required
def student_profile_view(request):
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, "Student profile not found for this account.")
        return redirect('dashboard')
    
    profile = request.user.student_profile
    projects = profile.projects.all()
    certifications = profile.certifications.all()
    documents = profile.documents.all()

    return render(request, 'students/profile.html', {
        'profile': profile,
        'projects': projects,
        'certifications': certifications,
        'documents': documents,
        'completion_percentage': profile.completion_percentage,
    })


@login_required
def student_edit_profile_view(request):
    if not hasattr(request.user, 'student_profile'):
        return redirect('dashboard')
    
    profile = request.user.student_profile

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your student profile has been updated successfully!")
            return redirect('student_profile')
        else:
            messages.error(request, "Please check form errors.")
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'students/edit_profile.html', {
        'form': form,
        'profile': profile
    })


@login_required
def resume_management_view(request):
    if not hasattr(request.user, 'student_profile'):
        return redirect('dashboard')

    profile = request.user.student_profile

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'upload':
            form = ResumeUploadForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                new_status = 'Updated' if profile.resume_file else 'Uploaded'
                profile.resume_status = new_status
                form.save()
                Notification.objects.create(
                    user=request.user,
                    title="Resume Updated",
                    message="Your placement resume has been uploaded/updated successfully.",
                    notification_type='SYSTEM',
                    link_url='/students/resume/'
                )
                messages.success(request, f"Resume successfully {new_status.lower()}!")
                return redirect('my_resume')

        elif action == 'delete':
            if profile.resume_file:
                profile.resume_file.delete(save=False)
                profile.resume_file = None
                profile.resume_status = 'Missing'
                profile.save()
                messages.info(request, "Resume removed. Please upload a new resume.")
                return redirect('my_resume')

    form = ResumeUploadForm(instance=profile)
    return render(request, 'students/resume_management.html', {
        'profile': profile,
        'form': form,
    })


@login_required
def add_project_view(request):
    if not hasattr(request.user, 'student_profile'):
        return redirect('dashboard')

    profile = request.user.student_profile
    if request.method == 'POST':
        form = StudentProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = profile
            project.save()
            messages.success(request, "Project added successfully!")
            return redirect('student_profile')
    return redirect('student_profile')


@login_required
def delete_project_view(request, project_id):
    if not hasattr(request.user, 'student_profile'):
        return redirect('dashboard')
    
    project = get_object_or_404(StudentProject, id=project_id, student=request.user.student_profile)
    project.delete()
    messages.info(request, "Project deleted.")
    return redirect('student_profile')


@login_required
def add_certification_view(request):
    if not hasattr(request.user, 'student_profile'):
        return redirect('dashboard')

    profile = request.user.student_profile
    if request.method == 'POST':
        form = StudentCertificationForm(request.POST)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.student = profile
            cert.save()
            messages.success(request, "Certification added successfully!")
            return redirect('student_profile')
    return redirect('student_profile')


@login_required
def delete_certification_view(request, cert_id):
    if not hasattr(request.user, 'student_profile'):
        return redirect('dashboard')
    
    cert = get_object_or_404(StudentCertification, id=cert_id, student=request.user.student_profile)
    cert.delete()
    messages.info(request, "Certification removed.")
    return redirect('student_profile')


@login_required
def documents_management_view(request):
    if not hasattr(request.user, 'student_profile'):
        return redirect('dashboard')

    profile = request.user.student_profile
    if request.method == 'POST':
        form = StudentDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.student = profile
            doc.save()
            messages.success(request, f"{doc.get_doc_type_display()} uploaded successfully!")
            return redirect('documents')
    else:
        form = StudentDocumentForm()

    documents = profile.documents.all()
    return render(request, 'students/documents.html', {
        'profile': profile,
        'documents': documents,
        'form': form,
    })


@login_required
def student_list_view(request):
    """Placement officer view to browse, search, and filter all registered students."""
    if not request.user.is_officer:
        return HttpResponseForbidden("Access restricted to Placement Officers & Administrators.")

    students = StudentProfile.objects.select_related('user').all()

    # Search query
    q = request.GET.get('q', '').strip()
    if q:
        students = students.filter(
            full_name__icontains=q
        ) | students.filter(
            roll_number__icontains=q
        ) | students.filter(
            skills__icontains=q
        )

    # Department filter
    dept = request.GET.get('dept', '').strip()
    if dept:
        students = students.filter(department=dept)

    # Year filter
    year = request.GET.get('year', '').strip()
    if year and year.isdigit():
        students = students.filter(current_year=int(year))

    # Placement status filter
    status = request.GET.get('status', '').strip()
    if status:
        students = students.filter(placement_status=status)

    # Min CGPA
    min_cgpa = request.GET.get('min_cgpa', '').strip()
    if min_cgpa:
        try:
            students = students.filter(cgpa__gte=float(min_cgpa))
        except ValueError:
            pass

    students = students.order_by('-cgpa', 'roll_number')
    paginator = Paginator(students, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'students/student_list.html', {
        'page_obj': page_obj,
        'q': q,
        'selected_dept': dept,
        'selected_year': year,
        'selected_status': status,
        'min_cgpa': min_cgpa,
        'total_count': students.count(),
    })


@login_required
def student_detail_view(request, student_id):
    """Placement officer view of a single student's complete placement dossier."""
    if not request.user.is_officer:
        return HttpResponseForbidden("Access restricted to Placement Officers.")

    student = get_object_or_404(StudentProfile, id=student_id)
    applications = student.applications.select_related('job', 'job__company').all()
    projects = student.projects.all()
    certifications = student.certifications.all()
    documents = student.documents.all()

    return render(request, 'students/student_detail.html', {
        'student': student,
        'applications': applications,
        'projects': projects,
        'certifications': certifications,
        'documents': documents,
    })
