# AI College Placement Management System 🎓💼

> *"Your Career Starts Here."*

A modern, full-stack, and AI-powered **College Placement Management Platform** designed for engineering and management institutions. Built with **Python Django**, **SQLite**, **HTML5/CSS3/JavaScript**, and an integrated **AI Career Assistant Engine**.

---

## 🌟 Key Features Overview

### 1. 🏠 Landing & Discovery Portal
- **Modern Collegiate Hero Section**: Features live placement statistics, headline metrics, and call-to-actions (*"Explore Jobs"*, *"Get Started"*).
- **Placement Statistics**: Displays real-time institutional metrics (Students Placed, Placement %, Highest & Average CTC).
- **Featured Partner Showcase**: Grid of premier recruiters (Microsoft, Amazon, TCS, Deloitte, IBM, Accenture, etc.).
- **Live Placement Drives**: Direct cards showing active recruitments, CTC packages, eligibility cutoffs, and application deadlines.
- **Campus Notice Board**: Dynamic announcements with pinned urgent alerts for aptitude tests and drive schedules.

### 2. 👨‍🎓 Student Management & Profiling
- **Secure Authentication & Registration**: Captures Full Name, Official College Email, Roll/USN Number, Branch/Department, Current Year, CGPA, Technical Skills, and Career Objectives.
- **Interactive Student Profile**:
  - **Dynamic Profile Completion Meter**: Visual progress indicator (e.g. `80% Completed`) prompting students to add projects, certifications, and links.
  - **Projects & Portfolios**: Showcase technical projects with GitHub links and live demos.
  - **Certifications**: Add credentials with verification links.
  - **Resume Management ("My Resume")**: Upload, replace, download, or delete official placement resumes with live status badges (`Uploaded`, `Missing`, `Updated`).
  - **Document Repository**: Upload marksheets, college ID proofs, and certificates.

### 3. 🏢 Company & Recruiter Management
- **Enterprise Profiles**: Comprehensive view of visiting companies with logos, description, classification (Product, Service, MNC, Startup, Consulting), CTC packages, and recruitment leads.
- **Officer Management**: Placement officers can register, edit, and manage partner companies directly from the dashboard or Django Admin.

### 4. 💼 Placement Drives & Automated Eligibility Checker
- **Job Discovery with Filters**: Search by keyword/skills, filter by department, location, job type (Full Time, Internship, Part Time), minimum salary package, and active status.
- **Smart Eligibility Verification**:
  - Automatically evaluates:
    - Minimum required CGPA vs Student CGPA
    - Permitted active backlogs
    - Eligible departments / branches
    - Eligible academic years
  - Real-time feedback:
    - ✅ *"You meet all mandatory eligibility criteria for this placement drive!"*
    - ❌ *"You are currently not eligible for this placement drive. Reason: Minimum required CGPA is 7.50, but your current CGPA is 7.10."*
- **1-Click Application**: Automatically links student's verified resume and prevents duplicate submissions.

### 5. 📊 Real-Time Application Tracking ("My Applications")
- Tracks candidate journey through standardized recruitment stages:
  - `Applied` (Blue)
  - `Shortlisted` (Purple)
  - `Aptitude Test` / `Technical Interview` / `HR Interview` (Orange / Amber)
  - `Selected / Placed` (Green)
  - `Rejected` (Red)
- Displays scheduled interview timings, venue, and meeting links.

### 6. 🤖 Dedicated AI Assistant Suite (`ai_assistant`)
- **AI Career Assistant Chat**: 24/7 interactive chat mentor with quick prompt chips (*"Find Jobs For Me"*, *"Check My Eligibility"*, *"Analyze My Resume"*, *"Prepare For Interview"*, *"Create Career Roadmap"*).
- **AI Job Recommendations ("Recommended For You")**: Analyzes student skills, CGPA, and branch to compute match compatibility % against active drives.
- **AI Resume Analyzer & ATS Scanner**: Evaluates resume text against high-demand tech keywords, calculates an ATS Score (out of 100), identifies detected skills, flags missing keywords, and offers specific improvements.
- **AI Job Description Matcher**: Compares candidate profile with pasted job descriptions to reveal Match % and skill gap recommendations.
- **AI Interview Preparation Simulator**: Company and role-specific question generator for Technical, HR, and Aptitude rounds with interactive answer evaluation and feedback.
- **AI Career Roadmaps**: Step-by-step milestone guides for **Python Developer**, **Full Stack Developer**, **Data Analyst**, **Data Engineer**, and **AI/ML Engineer**.
- **Graceful Fallback AI Architecture**: Works out-of-the-box with a built-in semantic matching engine, and seamlessly connects to **Google Gemini** or **OpenAI** when an API key is provided in `.env`.

### 7. 🏛️ Placement Officer & Admin Portal
- **Executive Analytics Dashboard**: High-level KPI cards (Total Students, Companies, Active Drives, Placed Count, CTC Distributions).
- **Interactive Chart.js Visualizations**: Department-wise placements, batch placement percentage doughnut chart, and package distribution bars.
- **Shortlisting & Candidate Management**: Filter applicants by drive, change statuses in real-time, schedule interview rounds, and record formal offers.
- **Automated Offer & Status Sync**: When a student is marked as `SELECTED`, their profile is updated to `PLACED` and an in-app celebratory notification is dispatched.

### 8. 📄 Data Reports & Accreditation Exports
- **Export Students Report (.xlsx)**: Excel spreadsheet of all student profiles, CGPAs, and placement statuses.
- **Export Companies Report (.xlsx)**: Excel summary of all visiting corporate partners.
- **Official Placement Dossier (.pdf)**: Formal printable PDF generated via **ReportLab** with official collegiate styling.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.14+, Django 6.1 (MVT Architecture) |
| **Database** | SQLite3 (Configurable to PostgreSQL / MySQL) |
| **Frontend** | HTML5, CSS3 (Modern Flexbox/Grid Design System), JavaScript (ES6+) |
| **Icons & Fonts** | FontAwesome 6, Google Fonts (*Plus Jakarta Sans* & *Inter*) |
| **Data Visualization** | Chart.js 4.x |
| **Document Export** | OpenPyXL (Excel), ReportLab (PDF) |
| **AI Integration** | Google Gemini API / OpenAI API with Built-in Fallback Semantic Engine |

---

## 🚀 Quick Start & Installation

### 1. Navigate to Project Directory
```bash
cd "placement_managementproject"
```

### 2. Install Dependencies (Pre-installed in environment)
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
A `.env` file is pre-configured in the project root:
```env
SECRET_KEY=django-insecure-vk76c2^=@^np4sodb1fl+9cng=n*3ydob765pw@wpnp*@x+p#)
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,*

# Optional: Add your Gemini or OpenAI API Key for real-time cloud LLM responses
# If left blank, the built-in Intelligent Fallback AI Engine will handle all queries
AI_API_KEY=
GEMINI_API_KEY=
OPENAI_API_KEY=
```

### 4. Apply Migrations & Seed Sample Data
```bash
python manage.py migrate
python manage.py seed_data
```

### 5. Run the Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```
Open your browser and navigate to: **`http://127.0.0.1:8000/`**

---

## 👥 Sample Login Credentials

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Placement Officer / Admin** | `admin` | `admin123` | Full access to Officer Dashboard, shortlisting, drives, and reports |
| **Student (Placed)** | `rahul` | `student123` | CSE Final Year, CGPA 8.75, Placed at Microsoft (₹18 LPA) |
| **Student (Selected)** | `priya` | `student123` | IT Final Year, CGPA 8.40, Selected at Deloitte (₹8.8 LPA) |
| **Student (Interviewing)** | `amit` | `student123` | AI & DS Final Year, CGPA 9.15, Interview scheduled at IBM |
| **Student (Shortlisted)** | `sneha` | `student123` | ECE Final Year, CGPA 7.60, Shortlisted for TCS |
| **Student (Applied)** | `rohit` | `student123` | CSE 3rd Year, CGPA 8.10, Applied for Accenture |

*(You can also register a brand new student account via `/accounts/register/`)*

---

## 📂 Project Architecture

```
placement_managementproject/
│
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── config/                      # Project Settings & Root Routing
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                    # Custom User Model & Authentication
│   ├── models.py                # CustomUser (Student, Officer, Admin)
│   ├── forms.py                 # Registration & Login Forms
│   ├── views.py
│   └── urls.py
│
├── students/                    # Student Profiles & Resume Management
│   ├── models.py                # StudentProfile, Project, Certification, Document
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── companies/                   # Corporate Partner Management
│   ├── models.py                # Company Model & CTC Stats
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── placements/                  # Placement Drives & Announcements
│   ├── models.py                # PlacementDrive (with Eligibility Logic), Announcement
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── applications/                # Applications, Shortlisting, & Interviews
│   ├── models.py                # JobApplication, InterviewSchedule, PlacementOffer
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── notifications/               # In-App Notification Center
│   ├── models.py                # Notification Model
│   ├── context_processors.py    # Unread Count Context Processor
│   ├── views.py
│   └── urls.py
│
├── ai_assistant/                # Dedicated Modular AI Engine
│   ├── services.py              # LLM Service (Gemini/OpenAI) + Smart Fallback Engine
│   ├── prompts.py               # Prompt Templates & Career Roadmaps
│   ├── models.py                # ResumeAnalysisLog, AIChatMessage
│   ├── views.py                 # Chat, Resume Analyzer, JD Matcher, Interview Sim
│   └── urls.py
│
├── core/                        # Home Landing, Dashboards, Reports, & Stats
│   ├── views.py                 # Home, Dashboards, Excel/PDF Exports, Errors
│   ├── urls.py
│   ├── tests.py                 # Automated Unit & Integration Test Suite
│   └── management/commands/     # seed_data Management Command
│
├── templates/                   # Clean, Modular Django HTML Templates
│   ├── base.html
│   ├── 404.html, 403.html, 500.html
│   ├── core/ (home, statistics, reports, contact)
│   ├── accounts/ (login, register)
│   ├── students/ (profile, edit_profile, resume_management, documents, list, detail)
│   ├── companies/ (company_list, company_detail, company_form, confirm_delete)
│   ├── placements/ (drive_list, drive_detail, drive_form, confirm_delete, calendar, announcements)
│   ├── applications/ (my_applications, officer_applications)
│   ├── dashboard/ (student_dashboard, officer_dashboard)
│   ├── notifications/ (notification_list)
│   └── ai_assistant/ (assistant, resume_analyzer, jd_analyzer, interview_prep, career_roadmap)
│
├── static/
│   ├── css/style.css            # Rich, Modern Design System & Responsive Layouts
│   ├── js/main.js               # Client Interactions, Dropdowns, AIChatEngine
│   └── images/
│
└── media/                       # Uploaded Files (Resumes, Photos, Documents, Logos)
```

---

## 🧪 Running Automated Tests

Run the built-in test suite covering models, views, eligibility checking, AI fallback logic, and report exports:
```bash
python manage.py test
```

---

## 🛡️ Security & Best Practices
- **Role-Based Access Control**: Placement officer functions (creating drives, shortlisting, scheduling interviews, downloading reports) are strictly protected.
- **CSRF Protection**: Enabled on all POST actions and AJAX chat requests.
- **Duplicate Application Prevention**: Enforced at both database model level (`unique_together = ('student', 'job')`) and view layer.
- **Graceful Error Handling**: Custom collegiate-themed `404.html`, `403.html`, and `500.html` error templates.
- **API Key Security**: Sensitive keys reside in `.env` and are never hardcoded into source code.
