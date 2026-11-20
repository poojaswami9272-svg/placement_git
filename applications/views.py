from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import JobApplication, InterviewSchedule, PlacementOffer
from .forms import ApplicationStatusUpdateForm, InterviewScheduleForm, PlacementOfferForm
from placements.models import PlacementDrive
from notifications.models import Notification

@login_required
def apply_job_view(request, drive_id):
    """Handles student applying for a placement drive."""
    if not hasattr(request.user, 'student_profile'):
        messages.error(request, "Only registered student profiles can apply for campus drives.")
        return redirect('drive_detail', drive_id=drive_id)

    profile = request.user.student_profile
    drive = get_object_or_404(PlacementDrive, id=drive_id)

    # 1. Check if application deadline passed
    if drive.is_expired:
        messages.error(request, "The application deadline for this drive has already passed.")
        return redirect('drive_detail', drive_id=drive_id)

    # 2. Check duplicate application
    if JobApplication.objects.filter(student=profile, job=drive).exists():
        messages.warning(request, "You have already applied for this placement drive.")
        return redirect('my_applications')

    # 3. Check student eligibility
    eligibility = drive.check_student_eligibility(profile)
    if not eligibility['is_eligible']:
        messages.error(request, f"You are not eligible to apply. Reason: {' '.join(eligibility['reasons'])}")
        return redirect('drive_detail', drive_id=drive_id)

    # 4. Create application
    application = JobApplication.objects.create(
        student=profile,
        job=drive,
        resume_file=profile.resume_file if profile.resume_file else None,
        status='APPLIED'
    )

    # Update profile placement status to APPLIED if still NOT_PLACED
    if profile.placement_status == 'NOT_PLACED':
        profile.placement_status = 'APPLIED'
        profile.save()

    # Create notification for student
    Notification.objects.create(
        user=request.user,
        title=f"Application Submitted: {drive.title}",
        message=f"Your application for {drive.title} at {drive.company.name} was successfully submitted.",
        notification_type='APPLICATION',
        link_url='/applications/my/'
    )

    messages.success(request, f"Application for {drive.title} at {drive.company.name} submitted successfully!")
    return redirect('my_applications')


@login_required
def my_applications_view(request):
    """Students' 'My Applications' page with status tracking, interview dates, and modern badges."""
    if not hasattr(request.user, 'student_profile'):
        return redirect('dashboard')

    profile = request.user.student_profile
    applications = JobApplication.objects.filter(student=profile).select_related('job', 'job__company').prefetch_related('interviews').order_by('-applied_date')

    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        applications = applications.filter(status=status_filter)

    # Counts summary
    total_apps = applications.count()
    shortlisted_count = applications.filter(status='SHORTLISTED').count()
    interview_count = applications.filter(status__in=['APTITUDE_TEST', 'TECHNICAL_INTERVIEW', 'HR_INTERVIEW']).count()
    selected_count = applications.filter(status='SELECTED').count()

    return render(request, 'applications/my_applications.html', {
        'applications': applications,
        'selected_status': status_filter,
        'total_apps': total_apps,
        'shortlisted_count': shortlisted_count,
        'interview_count': interview_count,
        'selected_count': selected_count,
    })


@login_required
def officer_applications_view(request):
    """Placement Officer view to review, filter, shortlist, and manage all student applications."""
    if not request.user.is_officer:
        return HttpResponseForbidden("Access restricted to Placement Officers.")

    applications = JobApplication.objects.select_related(
        'student', 'student__user', 'job', 'job__company'
    ).prefetch_related('interviews').all()

    # Search candidate or roll
    q = request.GET.get('q', '').strip()
    if q:
        applications = applications.filter(
            student__full_name__icontains=q
        ) | applications.filter(
            student__roll_number__icontains=q
        ) | applications.filter(
            job__title__icontains=q
        )

    # Filter by Drive / Job
    drive_id = request.GET.get('drive', '').strip()
    if drive_id and drive_id.isdigit():
        applications = applications.filter(job_id=int(drive_id))

    # Filter by Status
    status = request.GET.get('status', '').strip()
    if status:
        applications = applications.filter(status=status)

    # Filter by Department
    dept = request.GET.get('dept', '').strip()
    if dept:
        applications = applications.filter(student__department=dept)

    paginator = Paginator(applications, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_drives = PlacementDrive.objects.filter(is_active=True).select_related('company')

    return render(request, 'applications/officer_applications.html', {
        'page_obj': page_obj,
        'q': q,
        'selected_drive': drive_id,
        'selected_status': status,
        'selected_dept': dept,
        'all_drives': all_drives,
        'total_count': applications.count(),
    })


@login_required
def update_application_status_view(request, application_id):
    """Placement officer updates candidate application status."""
    if not request.user.is_officer:
        return HttpResponseForbidden("Access restricted.")

    application = get_object_or_404(JobApplication, id=application_id)
    if request.method == 'POST':
        form = ApplicationStatusUpdateForm(request.POST, instance=application)
        if form.is_valid():
            app = form.save()
            student = app.student
            # Synchronize student profile placement status
            if app.status == 'SELECTED':
                student.placement_status = 'PLACED'
                student.save()
                Notification.objects.create(
                    user=student.user,
                    title=f"🎉 Congratulations! You are Selected at {app.job.company.name}!",
                    message=f"We are delighted to announce that you have been selected for {app.job.title} at {app.job.company.name} with CTC ₹{app.job.salary_package} LPA!",
                    notification_type='SELECTION',
                    link_url='/applications/my/'
                )
            elif app.status == 'SHORTLISTED':
                if student.placement_status in ['NOT_PLACED', 'APPLIED']:
                    student.placement_status = 'SHORTLISTED'
                    student.save()
                Notification.objects.create(
                    user=student.user,
                    title=f"Application Shortlisted: {app.job.company.name}",
                    message=f"Congratulations! You have been shortlisted for {app.job.title} at {app.job.company.name}.",
                    notification_type='APPLICATION',
                    link_url='/applications/my/'
                )
            elif app.status in ['TECHNICAL_INTERVIEW', 'HR_INTERVIEW', 'APTITUDE_TEST']:
                if student.placement_status != 'PLACED':
                    student.placement_status = 'INTERVIEWING'
                    student.save()

            messages.success(request, f"Status for {student.full_name} updated to {app.get_status_display()}!")
            return redirect(request.POST.get('next') or 'officer_applications')

    return redirect('officer_applications')


@login_required
def schedule_interview_view(request, application_id):
    """Officer schedules an interview session for candidate."""
    if not request.user.is_officer:
        return HttpResponseForbidden("Access restricted.")

    application = get_object_or_404(JobApplication, id=application_id)
    if request.method == 'POST':
        form = InterviewScheduleForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()

            # Advance application status to the interview type if applicable
            if interview.interview_type == 'TECHNICAL_INTERVIEW':
                application.status = 'TECHNICAL_INTERVIEW'
            elif interview.interview_type == 'HR_INTERVIEW':
                application.status = 'HR_INTERVIEW'
            elif interview.interview_type in ['APTITUDE_TEST', 'CODING_TEST']:
                application.status = 'APTITUDE_TEST'
            application.save()

            if application.student.placement_status != 'PLACED':
                application.student.placement_status = 'INTERVIEWING'
                application.student.save()

            # Notify student
            Notification.objects.create(
                user=application.student.user,
                title=f"Interview Scheduled: {interview.title}",
                message=f"Your {interview.get_interview_type_display()} for {application.job.title} ({application.job.company.name}) is scheduled on {interview.interview_date} at {interview.interview_time}. Venue/Link: {interview.location_or_link}.",
                notification_type='INTERVIEW',
                link_url='/applications/my/'
            )

            messages.success(request, f"Interview scheduled for {application.student.full_name}!")
            return redirect(request.POST.get('next') or 'officer_applications')

    return redirect('officer_applications')


@login_required
def record_selection_view(request, application_id):
    """Record official placement offer when candidate is selected."""
    if not request.user.is_officer:
        return HttpResponseForbidden("Access restricted.")

    application = get_object_or_404(JobApplication, id=application_id)
    if request.method == 'POST':
        form = PlacementOfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.application = application
            offer.save()

            application.status = 'SELECTED'
            application.save()

            student = application.student
            student.placement_status = 'PLACED'
            student.save()

            Notification.objects.create(
                user=student.user,
                title=f"🎉 Formal Offer Extended: {application.job.company.name}",
                message=f"Official placement offer confirmed for role '{offer.job_role}' at {application.job.company.name} with CTC ₹{offer.package_offered} LPA!",
                notification_type='SELECTION',
                link_url='/applications/my/'
            )

            messages.success(request, f"Offer recorded and candidate {student.full_name} marked as PLACED!")
            return redirect('officer_applications')

    return redirect('officer_applications')
