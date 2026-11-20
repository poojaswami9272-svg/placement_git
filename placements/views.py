from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from .models import PlacementDrive, Announcement, EXPERIENCE_CHOICES
from .forms import PlacementDriveForm, AnnouncementForm
from companies.models import Company
from applications.models import JobApplication, InterviewSchedule
from notifications.models import Notification

def drive_list_view(request):
    """
    Job Discovery View with search by company, title, skills and
    filters by department, location, salary, job type, eligibility, experience.
    """
    drives = PlacementDrive.objects.filter(is_active=True).select_related('company')

    # Search keyword
    q = request.GET.get('q', '').strip()
    if q:
        drives = drives.filter(
            title__icontains=q
        ) | drives.filter(
            company__name__icontains=q
        ) | drives.filter(
            required_skills__icontains=q
        ) | drives.filter(
            description__icontains=q
        )

    # Filter by department
    dept = request.GET.get('dept', '').strip()
    if dept:
        drives = drives.filter(eligible_departments__icontains=dept)

    # Filter by location
    loc = request.GET.get('location', '').strip()
    if loc:
        drives = drives.filter(location__icontains=loc)

    # Filter by job type
    job_type = request.GET.get('job_type', '').strip()
    if job_type:
        drives = drives.filter(job_type=job_type)

    # Filter by experience requirement
    exp = request.GET.get('experience', '').strip()
    if exp:
        drives = drives.filter(experience_required=exp)

    # Filter by min salary package
    min_package = request.GET.get('min_package', '').strip()
    if min_package:
        try:
            drives = drives.filter(salary_package__gte=float(min_package))
        except ValueError:
            pass

    # Filter by only eligible for current student
    only_eligible = request.GET.get('only_eligible') == '1'
    student_profile = None
    applied_job_ids = set()

    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        student_profile = request.user.student_profile
        applied_job_ids = set(JobApplication.objects.filter(student=student_profile).values_list('job_id', flat=True))

        if only_eligible:
            # Filter in Python based on student eligibility criteria
            eligible_ids = []
            for d in drives:
                res = d.check_student_eligibility(student_profile)
                if res['is_eligible']:
                    eligible_ids.append(d.id)
            drives = drives.filter(id__in=eligible_ids)

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'package_high':
        drives = drives.order_by('-salary_package')
    elif sort_by == 'deadline':
        drives = drives.order_by('application_deadline')
    else:
        drives = drives.order_by('-created_at')

    # Popular companies
    popular_companies = Company.objects.all()[:8]

    # Upcoming drives (next 30 days)
    upcoming_drives = PlacementDrive.objects.filter(
        is_active=True,
        drive_date__gte=timezone.now().date()
    ).order_by('drive_date')[:4]

    paginator = Paginator(drives, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'placements/drive_list.html', {
        'page_obj': page_obj,
        'q': q,
        'selected_dept': dept,
        'selected_loc': loc,
        'selected_job_type': job_type,
        'selected_experience': exp,
        'experience_choices': EXPERIENCE_CHOICES,
        'min_package': min_package,
        'sort_by': sort_by,
        'only_eligible': only_eligible,
        'total_count': drives.count(),
        'popular_companies': popular_companies,
        'upcoming_drives': upcoming_drives,
        'applied_job_ids': applied_job_ids,
        'student_profile': student_profile,
    })


def drive_detail_view(request, drive_id):
    drive = get_object_or_404(PlacementDrive.objects.select_related('company'), id=drive_id)
    student_profile = None
    has_applied = False
    application = None
    eligibility_result = None

    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        student_profile = request.user.student_profile
        application = JobApplication.objects.filter(student=student_profile, job=drive).first()
        has_applied = application is not None
        eligibility_result = drive.check_student_eligibility(student_profile)

    # Other jobs from the same company
    other_jobs = PlacementDrive.objects.filter(company=drive.company, is_active=True).exclude(id=drive.id)[:3]

    return render(request, 'placements/drive_detail.html', {
        'drive': drive,
        'has_applied': has_applied,
        'application': application,
        'student_profile': student_profile,
        'eligibility_result': eligibility_result,
        'other_jobs': other_jobs,
    })


@login_required
def check_eligibility_ajax(request, drive_id):
    """AJAX endpoint for instant student eligibility check."""
    if not hasattr(request.user, 'student_profile'):
        return JsonResponse({'error': 'Only registered students can check eligibility'}, status=400)

    drive = get_object_or_404(PlacementDrive, id=drive_id)
    res = drive.check_student_eligibility(request.user.student_profile)
    return JsonResponse(res)


@login_required
def drive_create_view(request):
    if not request.user.is_officer:
        return HttpResponseForbidden("Only placement officers can post placement drives.")

    initial_company_id = request.GET.get('company')

    if request.method == 'POST':
        form = PlacementDriveForm(request.POST, request.FILES)
        if form.is_valid():
            drive = form.save()
            # Send notification to all registered students
            Notification.objects.bulk_create([
                Notification(
                    user=sp.user,
                    title=f"New Drive: {drive.title} at {drive.company.name}",
                    message=f"{drive.company.name} has announced a campus drive offering ₹{drive.salary_package} LPA. Deadline: {drive.application_deadline}.",
                    notification_type='DRIVE',
                    link_url=f"/jobs/{drive.id}/"
                )
                for sp in request.user.__class__.objects.filter(user_type='STUDENT')
            ])
            messages.success(request, f"Placement drive '{drive.title}' created and broadcasted successfully!")
            return redirect('drive_detail', drive_id=drive.id)
        else:
            messages.error(request, "Please fix errors in the form.")
    else:
        initial = {}
        if initial_company_id:
            initial['company'] = initial_company_id
        form = PlacementDriveForm(initial=initial)

    return render(request, 'placements/drive_form.html', {
        'form': form,
        'title': 'Create Placement Drive',
        'is_edit': False,
    })


@login_required
def drive_edit_view(request, drive_id):
    if not request.user.is_officer:
        return HttpResponseForbidden("Only placement officers can edit drives.")

    drive = get_object_or_404(PlacementDrive, id=drive_id)
    if request.method == 'POST':
        form = PlacementDriveForm(request.POST, request.FILES, instance=drive)
        if form.is_valid():
            form.save()
            messages.success(request, f"Placement drive '{drive.title}' updated successfully!")
            return redirect('drive_detail', drive_id=drive.id)
        else:
            messages.error(request, "Please check errors in the form.")
    else:
        form = PlacementDriveForm(instance=drive)

    return render(request, 'placements/drive_form.html', {
        'form': form,
        'drive': drive,
        'title': f'Edit Drive: {drive.title}',
        'is_edit': True,
    })


@login_required
def drive_delete_view(request, drive_id):
    if not request.user.is_officer:
        return HttpResponseForbidden("Only placement officers can delete drives.")

    drive = get_object_or_404(PlacementDrive, id=drive_id)
    if request.method == 'POST':
        title = drive.title
        drive.delete()
        messages.info(request, f"Placement drive '{title}' has been deleted.")
        return redirect('drive_list')

    return render(request, 'placements/drive_confirm_delete.html', {'drive': drive})


def calendar_view(request):
    """
    Placement Drive Calendar showing upcoming drives, aptitude tests,
    interviews, and company visits.
    """
    today = timezone.now().date()
    upcoming_drives = PlacementDrive.objects.filter(is_active=True, drive_date__gte=today).order_by('drive_date')
    deadlines = PlacementDrive.objects.filter(is_active=True, application_deadline__gte=today).order_by('application_deadline')
    
    interviews = []
    if request.user.is_authenticated:
        if request.user.is_student:
            interviews = InterviewSchedule.objects.filter(
                application__student=request.user.student_profile,
                interview_date__gte=today
            ).select_related('application', 'application__job', 'application__job__company')
        elif request.user.is_officer:
            interviews = InterviewSchedule.objects.filter(
                interview_date__gte=today
            ).select_related('application', 'application__student', 'application__job', 'application__job__company')

    return render(request, 'placements/calendar.html', {
        'upcoming_drives': upcoming_drives,
        'deadlines': deadlines,
        'interviews': interviews,
        'today': today,
    })


def announcements_view(request):
    """List of all campus placement announcements and notices."""
    announcements = Announcement.objects.all().order_by('-is_pinned', '-created_at')
    
    if request.method == 'POST' and request.user.is_authenticated and request.user.is_officer:
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save()
            messages.success(request, "Announcement published to campus board!")
            return redirect('announcements')
    else:
        form = AnnouncementForm()

    return render(request, 'placements/announcements.html', {
        'announcements': announcements,
        'form': form,
    })
