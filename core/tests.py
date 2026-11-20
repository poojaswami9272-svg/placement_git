from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser
from students.models import StudentProfile
from companies.models import Company
from placements.models import PlacementDrive
from applications.models import JobApplication
from ai_assistant.services import AIAssistantService, ResumeAnalyzerService, JobDescriptionMatcherService

class PlacementSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test officer user
        self.officer = CustomUser.objects.create_user(
            username='officer1',
            email='officer@college.edu',
            password='password123',
            user_type='OFFICER',
            is_staff=True
        )

        # Create test student user and profile
        self.student_user = CustomUser.objects.create_user(
            username='student1',
            email='student1@college.edu',
            password='password123',
            user_type='STUDENT'
        )
        self.student_profile = StudentProfile.objects.create(
            user=self.student_user,
            roll_number='21CS101',
            full_name='Test Student',
            department='CSE',
            current_year=4,
            cgpa=8.50,
            skills='Python, Django, SQL, Git',
            active_backlogs=0
        )

        # Create test company
        self.company = Company.objects.create(
            name='TestTech Global',
            industry='Software',
            company_type='PRODUCT',
            location='Bangalore',
            average_package=10.0,
            highest_package=15.0
        )

        # Create test placement drive
        self.drive = PlacementDrive.objects.create(
            company=self.company,
            title='Junior Python Engineer',
            job_type='FULL_TIME',
            salary_package=10.0,
            minimum_cgpa=7.5,
            max_backlogs=0,
            eligible_departments='CSE,IT,AI_DS',
            eligible_years='4',
            required_skills='Python, Django, SQL',
            vacancies=5,
            application_deadline=timezone.now().date() + timedelta(days=10),
            drive_date=timezone.now().date() + timedelta(days=20),
            description='Test job description'
        )

    def test_home_page_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI College Placement Management System')

    def test_job_discovery_list(self):
        response = self.client.get(reverse('drive_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Junior Python Engineer')
        self.assertContains(response, 'TestTech Global')

    def test_eligibility_checker_eligible(self):
        res = self.drive.check_student_eligibility(self.student_profile)
        self.assertTrue(res['is_eligible'])
        self.assertIn("Python", res['matched_skills'])

    def test_eligibility_checker_ineligible_cgpa(self):
        # Set high minimum CGPA
        self.drive.minimum_cgpa = 9.0
        self.drive.save()
        res = self.drive.check_student_eligibility(self.student_profile)
        self.assertFalse(res['is_eligible'])
        self.assertTrue(any('CGPA' in r for r in res['reasons']))

    def test_job_application_submission_and_duplicate_prevention(self):
        self.client.login(username='student1', password='password123')
        # Apply for job
        apply_url = reverse('apply_job', args=[self.drive.id])
        response = self.client.post(apply_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(JobApplication.objects.filter(student=self.student_profile, job=self.drive).exists())

        # Duplicate application attempt
        dup_response = self.client.post(apply_url, follow=True)
        self.assertEqual(JobApplication.objects.filter(student=self.student_profile, job=self.drive).count(), 1)

    def test_student_dashboard(self):
        self.client.login(username='student1', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recommended For You')

    def test_officer_dashboard(self):
        self.client.login(username='officer1', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Placement Administration Hub')

    def test_ai_chat_fallback_service(self):
        reply = AIAssistantService.generate_chat_reply("I know Python, Django and SQL. Which jobs should I apply for?", self.student_profile)
        self.assertIn("Recommended", reply)

    def test_ai_resume_analyzer_service(self):
        resume_text = "Proficient in Python, Django, SQL, PostgreSQL, Docker, Git. Built REST API applications with high scalability."
        analysis = ResumeAnalyzerService.analyze_resume_text(resume_text, "Python Developer")
        self.assertGreaterEqual(analysis['score'], 60)
        self.assertIn('Python', analysis['skills_found'])

    def test_ai_jd_matcher_service(self):
        jd_text = "Looking for a Python Developer with experience in Django, SQL, and Docker."
        student_skills = ['Python', 'Django', 'SQL']
        res = JobDescriptionMatcherService.match_jd_with_student(jd_text, student_skills)
        self.assertGreaterEqual(res['match_percentage'], 70)
        self.assertIn('Python', res['matching_skills'])

    def test_reports_excel_export(self):
        self.client.login(username='officer1', password='password123')
        response = self.client.get(reverse('export_students_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def test_reports_pdf_export(self):
        self.client.login(username='officer1', password='password123')
        response = self.client.get(reverse('export_placements_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], "application/pdf")
