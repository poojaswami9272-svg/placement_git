from django.db import models
from django.utils import timezone
from companies.models import Company

JOB_TYPE_CHOICES = (
    ('FULL_TIME', 'Full Time'),
    ('INTERNSHIP', 'Internship'),
    ('INTERNSHIP_FULL_TIME', 'Internship + Full Time'),
    ('PART_TIME', 'Part Time'),
)

EXPERIENCE_CHOICES = (
    ('FRESHER', 'Fresher (0 Years)'),
    ('0_TO_1_YEAR', '0 to 1 Year'),
    ('1_TO_2_YEARS', '1 to 2 Years'),
    ('1_TO_3_YEARS', '1 to 3 Years'),
    ('2_TO_4_YEARS', '2 to 4 Years'),
    ('3_PLUS_YEARS', '3+ Years'),
)

ANNOUNCEMENT_CATEGORY_CHOICES = (
    ('DRIVE', 'New Placement Drive'),
    ('INTERVIEW', 'Interview Announcement'),
    ('VISIT', 'Company Campus Visit'),
    ('TEST', 'Aptitude / Coding Test'),
    ('NOTICE', 'Important Notice'),
    ('DEADLINE', 'Deadline Reminder'),
)

class PlacementDrive(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='placement_drives')
    title = models.CharField(max_length=200)
    job_type = models.CharField(max_length=30, choices=JOB_TYPE_CHOICES, default='FULL_TIME')
    experience_required = models.CharField(
        max_length=30,
        choices=EXPERIENCE_CHOICES,
        default='1_TO_3_YEARS',
        help_text="Required job experience"
    )
    description = models.TextField()
    location = models.CharField(max_length=150, default='Bangalore / Remote')
    salary_package = models.DecimalField(max_digits=5, decimal_places=2, help_text="In LPA (Lakhs per Annum)")
    minimum_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=6.50)
    max_backlogs = models.IntegerField(default=0, help_text="Maximum active backlogs allowed")
    eligible_departments = models.CharField(
        max_length=255,
        default='CSE,IT,AI_DS,ECE,EEE,MECH,CIVIL,MCA,MBA',
        help_text="Comma-separated department codes"
    )
    eligible_years = models.CharField(
        max_length=50,
        default='3,4',
        help_text="Comma-separated eligible student years e.g. 3,4"
    )
    required_skills = models.TextField(help_text="Comma-separated skills e.g. Python, SQL, Django, Git")
    vacancies = models.PositiveIntegerField(default=10)
    application_deadline = models.DateField()
    drive_date = models.DateField()
    selection_process = models.TextField(
        default="1. Online Aptitude & Coding Test\n2. Technical Round 1\n3. Technical Round 2\n4. HR Interview"
    )
    banner_image = models.ImageField(upload_to='job_banners/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    @property
    def is_expired(self):
        return self.application_deadline < timezone.now().date()

    @property
    def skills_list(self):
        if not self.required_skills:
            return []
        return [s.strip() for s in self.required_skills.split(',') if s.strip()]

    @property
    def departments_list(self):
        if not self.eligible_departments:
            return []
        return [d.strip() for d in self.eligible_departments.split(',') if d.strip()]

    @property
    def years_list(self):
        if not self.eligible_years:
            return []
        return [int(y.strip()) for y in self.eligible_years.split(',') if y.strip().isdigit()]

    def check_student_eligibility(self, student_profile):
        """
        Evaluates student profile against drive requirements.
        Returns:
            dict with:
                - is_eligible (bool)
                - status_message (str)
                - reasons (list of failure reasons if any)
                - matched_skills (list of matched skills)
                - missing_skills (list of missing skills)
        """
        reasons = []
        is_eligible = True

        # 1. CGPA check
        if student_profile.cgpa < self.minimum_cgpa:
            is_eligible = False
            reasons.append(f"Minimum required CGPA is {self.minimum_cgpa:.2f}, but your current CGPA is {student_profile.cgpa:.2f}.")

        # 2. Backlogs check
        if student_profile.active_backlogs > self.max_backlogs:
            is_eligible = False
            reasons.append(f"Drive permits at most {self.max_backlogs} backlogs; you currently have {student_profile.active_backlogs}.")

        # 3. Department check
        eligible_depts = self.departments_list
        if eligible_depts and student_profile.department not in eligible_depts:
            is_eligible = False
            reasons.append(f"Department '{student_profile.get_department_display()}' is not listed among eligible departments ({', '.join(eligible_depts)}).")

        # 4. Year check
        eligible_yrs = self.years_list
        if eligible_yrs and student_profile.current_year not in eligible_yrs:
            is_eligible = False
            reasons.append(f"Eligible for year(s) {', '.join(str(y) for y in eligible_yrs)}, but you are currently in year {student_profile.current_year}.")

        # 5. Skills analysis
        student_skills_lower = [s.lower() for s in student_profile.skills_list]
        matched_skills = []
        missing_skills = []

        for req in self.skills_list:
            if any(req.lower() in s or s in req.lower() for s in student_skills_lower):
                matched_skills.append(req)
            else:
                missing_skills.append(req)

        # Notice: lack of optional skills doesn't strictly block application unless core eligibility fails,
        # but provides guidance.
        if is_eligible:
            status_message = "You meet all mandatory eligibility criteria for this placement drive!"
        else:
            status_message = "You are currently not eligible for this placement drive."

        return {
            'is_eligible': is_eligible,
            'status_message': status_message,
            'reasons': reasons,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
        }


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=ANNOUNCEMENT_CATEGORY_CHOICES, default='NOTICE')
    content = models.TextField()
    related_job = models.ForeignKey(PlacementDrive, on_delete=models.SET_NULL, null=True, blank=True, related_name='announcements')
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"
