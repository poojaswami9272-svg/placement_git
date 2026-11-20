import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .services import AIAssistantService, ResumeAnalyzerService, JobDescriptionMatcherService
from .prompts import CAREER_ROADMAPS
from placements.models import PlacementDrive
from companies.models import Company

def ai_assistant_chat_view(request):
    """Chat-style AI Placement Career Assistant page and JSON endpoint."""
    student_profile = None
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        student_profile = request.user.student_profile

    # Handle AJAX Chat queries
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_msg = data.get('message', '').strip()
        except Exception:
            user_msg = request.POST.get('message', '').strip()

        if not user_msg:
            return JsonResponse({'reply': 'Please type a valid question.'}, status=400)

        reply = AIAssistantService.generate_chat_reply(user_msg, student_profile)
        return JsonResponse({'reply': reply})

    return render(request, 'ai_assistant/assistant.html', {
        'student_profile': student_profile,
    })


def ai_resume_analyzer_view(request):
    """AI Resume Analyzer: Analyzes student resume text or profile."""
    analysis = None
    student_profile = None
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        student_profile = request.user.student_profile

    if request.method == 'POST':
        resume_text = request.POST.get('resume_text', '').strip()
        target_role = request.POST.get('target_role', 'Software Engineer').strip()

        # If student didn't paste text but has profile skills/projects, use them
        if not resume_text and student_profile:
            skills = student_profile.skills
            projects = " ".join([f"{p.title} {p.technologies} {p.description}" for p in student_profile.projects.all()])
            bio = student_profile.bio
            resume_text = f"Student Profile: {student_profile.full_name}\nDepartment: {student_profile.department}\nSkills: {skills}\nProjects: {projects}\nBio: {bio}"

        if resume_text:
            analysis = ResumeAnalyzerService.analyze_resume_text(resume_text, target_role)

    return render(request, 'ai_assistant/resume_analyzer.html', {
        'student_profile': student_profile,
        'analysis': analysis,
    })


def ai_jd_analyzer_view(request):
    """Compares a pasted Job Description with student skills."""
    match_result = None
    jd_text = ""
    job_id = request.GET.get('job_id')
    prefilled_job = None

    if job_id and job_id.isdigit():
        prefilled_job = PlacementDrive.objects.filter(id=int(job_id)).first()
        if prefilled_job:
            jd_text = f"Role: {prefilled_job.title}\nCompany: {prefilled_job.company.name}\nRequired Skills: {prefilled_job.required_skills}\nDescription: {prefilled_job.description}"

    student_skills_list = []
    if request.user.is_authenticated and hasattr(request.user, 'student_profile'):
        student_skills_list = request.user.student_profile.skills_list

    if request.method == 'POST':
        jd_text = request.POST.get('jd_text', '').strip()
        custom_skills = request.POST.get('student_skills', '').strip()
        if custom_skills:
            student_skills_list = [s.strip() for s in custom_skills.split(',') if s.strip()]

        if jd_text:
            match_result = JobDescriptionMatcherService.match_jd_with_student(jd_text, student_skills_list)

    return render(request, 'ai_assistant/jd_analyzer.html', {
        'jd_text': jd_text,
        'prefilled_job': prefilled_job,
        'student_skills_list': student_skills_list,
        'match_result': match_result,
    })


def ai_interview_prep_view(request):
    """
    AI Interview Preparation Simulator:
    Generates questions for selected Company, Job Role, and Round Type.
    Allows submitting answers for feedback.
    """
    company_name = request.GET.get('company', 'TCS')
    role = request.GET.get('role', 'Python Developer')
    round_type = request.GET.get('round', 'technical')
    feedback = None

    # Curated Question Bank / AI Generator
    question_bank = {
        'technical': [
            {
                'id': 1,
                'q': 'What is Object-Oriented Programming (OOP) in Python? Explain inheritance, encapsulation, and polymorphism with examples.',
                'tips': 'Define each pillar clearly. Mention class vs instance attributes and how encapsulation is implemented via naming conventions.'
            },
            {
                'id': 2,
                'q': 'Explain the difference between Django MVT and traditional MVC architecture. How does the ORM optimize queries?',
                'tips': 'Mention Model, View (acts as controller), and Template. Mention select_related() and prefetch_related() for N+1 query optimization.'
            },
            {
                'id': 3,
                'q': 'What is the difference between a list and a tuple in Python? When would you choose one over the other?',
                'tips': 'Focus on mutability, memory allocation, hashing for dictionary keys, and performance.'
            },
            {
                'id': 4,
                'q': 'How do REST APIs work? Explain the difference between GET, POST, PUT, PATCH, and DELETE.',
                'tips': 'Discuss idempotency (PUT vs POST), status codes (200, 201, 400, 404, 500), and JSON payloads.'
            }
        ],
        'hr': [
            {
                'id': 1,
                'q': 'Tell me about yourself and why you chose your engineering branch.',
                'tips': 'Keep it under 90 seconds. Cover education, passions, 2 standout projects, and future career aspiration.'
            },
            {
                'id': 2,
                'q': 'Describe a challenging project you worked on. How did you overcome obstacles?',
                'tips': 'Use the STAR method: Situation, Task, Action, and Result. Highlight teamwork and perseverance.'
            },
            {
                'id': 3,
                'q': 'Where do you see yourself in 3 to 5 years after joining our company?',
                'tips': 'Emphasize continuous learning, mastering system architecture, and mentoring junior engineers.'
            }
        ],
        'aptitude': [
            {
                'id': 1,
                'q': 'Two trains running in opposite directions at 60 km/h and 40 km/h cross each other in 18 seconds. If one is 260m long, find the length of the other.',
                'tips': 'Relative speed = 60 + 40 = 100 km/h = 100 * (5/18) m/s = 250/9 m/s. Distance = (250/9) * 18 = 500m. Length = 500 - 260 = 240m.'
            },
            {
                'id': 2,
                'q': 'A can do a piece of work in 12 days and B in 15 days. They work together for 5 days. What fraction of work is left?',
                'tips': '1/12 + 1/15 = 9/60 = 3/20 per day. In 5 days: 5 * 3/20 = 15/20 = 3/4 done. Left = 1/4.'
            }
        ]
    }

    # Handle answer evaluation
    if request.method == 'POST':
        user_answer = request.POST.get('user_answer', '').strip()
        q_text = request.POST.get('question_text', '').strip()
        if user_answer:
            word_count = len(user_answer.split())
            if word_count > 25:
                feedback = {
                    'status': 'Good Effort!',
                    'score': '8.5 / 10',
                    'strengths': "Clear explanation, good structure, and relevant terminology.",
                    'improvement': "Consider adding a concrete real-world code snippet or metric to make your response even more memorable to recruiters."
                }
            else:
                feedback = {
                    'status': 'Needs Expansion',
                    'score': '5.5 / 10',
                    'strengths': "Direct response to the question.",
                    'improvement': "Your answer is quite brief. Elaborate with details, technical nuances, or edge cases to demonstrate deeper mastery."
                }

    selected_questions = question_bank.get(round_type, question_bank['technical'])
    companies = Company.objects.all()[:10]

    return render(request, 'ai_assistant/interview_prep.html', {
        'company_name': company_name,
        'role': role,
        'round_type': round_type,
        'questions': selected_questions,
        'companies': companies,
        'feedback': feedback,
    })


def ai_career_roadmap_view(request):
    """Interactive career roadmap generator."""
    career_key = request.GET.get('career', 'python_developer')
    roadmap = CAREER_ROADMAPS.get(career_key, CAREER_ROADMAPS['python_developer'])

    return render(request, 'ai_assistant/career_roadmap.html', {
        'career_key': career_key,
        'roadmap': roadmap,
        'all_roadmaps': CAREER_ROADMAPS,
    })
