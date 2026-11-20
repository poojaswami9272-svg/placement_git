import os
import re
import json
import requests
from django.conf import settings
from .prompts import SYSTEM_PROMPT, CAREER_ROADMAPS
from placements.models import PlacementDrive
from companies.models import Company

class AIAssistantService:
    """
    Modular AI Service supporting Google Gemini API or OpenAI API,
    with an intelligent, context-aware fallback engine when no key is set.
    """

    @classmethod
    def get_api_key(cls):
        return os.getenv('GEMINI_API_KEY') or os.getenv('AI_API_KEY') or os.getenv('OPENAI_API_KEY') or ''

    @classmethod
    def generate_chat_reply(cls, user_message, student_profile=None):
        api_key = cls.get_api_key()
        msg_lower = user_message.lower()

        # If Gemini API Key is available, attempt real cloud LLM call
        if api_key and (api_key.startswith('AIza') or len(api_key) > 30):
            try:
                endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                context_prefix = ""
                if student_profile:
                    context_prefix = (
                        f"Student Context: Name: {student_profile.full_name}, Dept: {student_profile.department}, "
                        f"Year: {student_profile.current_year}, CGPA: {student_profile.cgpa}, "
                        f"Skills: {student_profile.skills}, Interests: {student_profile.career_interests}.\n"
                    )

                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"{SYSTEM_PROMPT}\n\n{context_prefix}\nStudent Inquiry: {user_message}"
                        }]
                    }]
                }
                res = requests.post(endpoint, json=payload, timeout=6)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get('candidates', [])
                    if candidates and 'content' in candidates[0]:
                        parts = candidates[0]['content'].get('parts', [])
                        if parts:
                            return parts[0].get('text', '')
            except Exception:
                pass # Gracefully fall back to local intelligent engine

        # Intelligent Context-Aware Fallback Engine
        return cls._intelligent_fallback_response(user_message, msg_lower, student_profile)

    @classmethod
    def _intelligent_fallback_response(cls, raw_msg, msg, profile):
        # 1. Job search / "Which jobs should I apply for"
        if any(w in msg for w in ['find job', 'which job', 'recommend job', 'suitable job', 'apply for', 'opening']):
            drives = PlacementDrive.objects.filter(is_active=True).select_related('company')[:4]
            if not drives.exists():
                return "There are currently no active placement drives published. Please check back soon or contact the placement cell!"

            reply = "### 🎯 Recommended Placement Drives for You\n\nBased on current campus openings, here are the top matching opportunities:\n\n"
            for d in drives:
                reply += f"- **{d.title}** at **{d.company.name}**\n"
                reply += f"  - **CTC Package**: ₹{d.salary_package} LPA\n"
                reply += f"  - **Min CGPA**: {d.minimum_cgpa} | **Eligible**: {d.eligible_departments}\n"
                reply += f"  - **Required Skills**: `{d.required_skills}`\n"
                reply += f"  - [👉 View Details & Apply](/jobs/{d.id}/)\n\n"
            reply += "Would you like me to check your specific eligibility for any of these companies or help you prepare for technical rounds?"
            return reply

        # 2. Eligibility question
        if 'eligib' in msg or 'can i apply' in msg or 'cgpa' in msg:
            if profile:
                return (
                    f"### 📋 Your Placement Eligibility Status\n\n"
                    f"- **Current CGPA**: `{profile.cgpa} / 10.0`\n"
                    f"- **Department**: `{profile.get_department_display()}`\n"
                    f"- **Academic Year**: `Year {profile.current_year}`\n"
                    f"- **Active Backlogs**: `{profile.active_backlogs}`\n\n"
                    f"Most tier-1 companies require a minimum **CGPA of 7.0 to 7.5** with **0 active backlogs**. "
                    f"You can instantly verify your eligibility on any job page by clicking the **'Check My Eligibility'** button!"
                )
            return "To check your specific eligibility, please log in with your student account. Our system automatically checks your CGPA, branch, and backlogs against each company's recruitment criteria!"

        # 3. Resume / Resume tips
        if 'resume' in msg:
            return (
                "### 📄 AI Resume Optimization Tips for Campus Placements\n\n"
                "1. **Use the STAR Method**: Format project bullet points as *Situation, Task, Action, and Result*.\n"
                "2. **Quantify Achievements**: Instead of *'built web app'*, write *'Developed Django REST API handling 100+ requests with 99% uptime'*.\n"
                "3. **Highlight Core Tech Stack**: Put your strongest technologies (e.g. Python, SQL, Git, Docker) right below education.\n"
                "4. **Include Live Links**: Ensure every major project has a GitHub link and working demo URL.\n\n"
                "💡 **Try this now**: Visit our **[AI Resume Analyzer](/ai/resume-analyzer/)** to get an automated score out of 100 and identify missing skills!"
            )

        # 4. Specific role queries (e.g. Data Engineer, Data Analyst, Python Developer)
        if 'data engineer' in msg:
            return (
                "### 🛠️ How to Prepare for a Data Engineer Role\n\n"
                "Data Engineers design, construct, and maintain data pipelines and architectures. Here is your roadmap:\n\n"
                "- **Key Technologies to Master**: Advanced SQL, Python (Pandas/PySpark), Apache Airflow, Snowflake/PostgreSQL, Docker, AWS S3/Glue.\n"
                "- **Recommended Projects**: Build an automated ETL pipeline that extracts API data, transforms it with Python, and loads it into a cloud data warehouse.\n"
                "- **Target Companies**: Deloitte, Accenture, Amazon, Infosys, IBM.\n\n"
                "👉 Visit **[AI Career Roadmaps](/ai/career-roadmap/?career=data_engineer)** for the complete 8-step roadmap!"
            )

        if 'data analyst' in msg:
            return (
                "### 📊 Pathway to Becoming a Data Analyst\n\n"
                "- **Key Technologies**: SQL (Window functions, Joins, Aggregations), Power BI / Tableau, Python (Pandas, Matplotlib), Advanced Excel.\n"
                "- **Core Competencies**: Business acumen, statistical hypothesis testing, data visualization storytelling.\n"
                "- **Target Companies**: Deloitte, Cognizant, TCS, Capgemini, Fintech startups.\n\n"
                "👉 Explore the full **[Data Analyst Career Roadmap](/ai/career-roadmap/?career=data_analyst)**!"
            )

        if 'python' in msg or 'django' in msg:
            return (
                "### 🐍 Excelling as a Python / Django Developer\n\n"
                "- **Core Skills Required**: Python 3 OOP, Django MVT & ORM, Django REST Framework, PostgreSQL, Git, Docker, Unit Testing.\n"
                "- **Top Project Ideas**: Full-stack Job Placement Portal, E-Commerce API with JWT Auth, Real-time Chat using WebSockets.\n"
                "- **Campus Interview Focus**: List vs Tuple, Generators vs Iterators, Django QuerySet evaluation, REST API status codes.\n\n"
                "👉 Head over to **[AI Interview Preparation](/ai/interview-prep/)** to practice technical questions!"
            )

        # 5. Interview preparation general
        if 'interview' in msg or 'prepare' in msg or 'question' in msg:
            return (
                "### 💼 Campus Placement Interview Master Checklist\n\n"
                "1. **Round 1 (Aptitude & Coding)**: Quantitative aptitude, logical reasoning, and 2 DSA coding problems.\n"
                "2. **Round 2 (Technical Discussion)**: Deep dive into your primary programming language, database normalization, SQL queries, and project architecture.\n"
                "3. **Round 3 (HR & Behavioral)**: 'Tell me about yourself', conflict resolution, handling deadlines, and why you want to join the company.\n\n"
                "👉 Use our dedicated **[AI Interview Preparation Simulator](/ai/interview-prep/)** to get mock questions tailored to your target company!"
            )

        # General welcoming reply
        return (
            "### 👋 Hello! I'm your AI College Placement Assistant\n\n"
            "I'm here to help you accelerate your campus placement journey. Here are some things you can ask me:\n\n"
            "- *'I know Python, Django and SQL. Which jobs should I apply for?'*\n"
            "- *'How can I become a Data Engineer or Cloud Developer?'*\n"
            "- *'Check my placement eligibility and required CGPA.'*\n"
            "- *'Analyze my resume and suggest missing skills.'*\n"
            "- *'Give me technical interview questions for TCS, Microsoft, or Infosys.'*\n\n"
            "Feel free to type your question below or click any of the quick prompts on the left!"
        )


class ResumeAnalyzerService:
    """Evaluates student resumes against industry keywords and returns scores."""

    TECH_KEYWORDS = {
        'Python', 'Django', 'FastAPI', 'Flask', 'Java', 'Spring Boot', 'C++',
        'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis',
        'JavaScript', 'TypeScript', 'React', 'HTML5', 'CSS3', 'Next.js',
        'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Linux', 'Git', 'GitHub',
        'REST API', 'GraphQL', 'Microservices', 'CI/CD', 'Pandas', 'NumPy',
        'Machine Learning', 'Data Structures', 'Algorithms', 'OOP'
    }

    @classmethod
    def analyze_resume_text(cls, text_content, target_role="Software Engineer"):
        found = set()
        for kw in cls.TECH_KEYWORDS:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text_content, re.IGNORECASE):
                found.add(kw)

        # Base scoring algorithm
        base_score = 50
        keyword_score = min(len(found) * 4, 35)
        length_score = 15 if len(text_content.split()) >= 150 else 5
        total_score = min(base_score + keyword_score + length_score, 98)

        missing = sorted(list(cls.TECH_KEYWORDS - found))[:6]

        recommendations = [
            f"Incorporate high-demand backend skills like {', '.join(missing[:3])}.",
            "Quantify results in your project descriptions using percentages or user metrics (e.g. 'improved performance by 25%').",
            "Include your GitHub and LinkedIn profile links in the header section.",
            f"Tailor your profile summary specifically toward the {target_role} role."
        ]

        return {
            'score': total_score,
            'skills_found': sorted(list(found)),
            'missing_skills': missing,
            'recommendations': recommendations,
        }


class JobDescriptionMatcherService:
    """Matches a job description text against candidate's skills."""

    @classmethod
    def match_jd_with_student(cls, jd_text, student_skills_list):
        jd_words = set(re.findall(r'\b[a-zA-Z0-9\+\#\.]+\b', jd_text.lower()))
        student_skills_lower = {s.lower() for s in student_skills_list}

        # Common tech keywords
        common_tech = [
            'python', 'django', 'sql', 'javascript', 'react', 'java', 'aws',
            'docker', 'git', 'rest api', 'postgresql', 'c++', 'linux', 'html', 'css'
        ]

        req_skills_in_jd = []
        for tech in common_tech:
            if tech in jd_text.lower():
                req_skills_in_jd.append(tech)

        if not req_skills_in_jd:
            req_skills_in_jd = ['python', 'sql', 'git', 'problem solving']

        matching = []
        missing = []

        for req in req_skills_in_jd:
            if any(req in s or s in req for s in student_skills_lower):
                matching.append(req.title())
            else:
                missing.append(req.title())

        total = len(req_skills_in_jd)
        match_percentage = int((len(matching) / total) * 100) if total > 0 else 70
        match_percentage = max(min(match_percentage, 95), 35)

        return {
            'match_percentage': match_percentage,
            'matching_skills': matching,
            'skills_to_improve': missing,
            'recommendation': "Add projects featuring missing technologies to increase shortlist chances!" if missing else "Your profile is a strong fit for this position!"
        }
