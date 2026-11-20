from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date, time
from accounts.models import CustomUser
from students.models import StudentProfile, StudentProject, StudentCertification
from companies.models import Company
from placements.models import PlacementDrive, Announcement
from applications.models import JobApplication, InterviewSchedule, PlacementOffer
from notifications.models import Notification

class Command(BaseCommand):
    help = "Populate realistic sample data for AI College Placement Management System"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding comprehensive campus placement data..."))

        # 1. Create Placement Officer / Admin User
        admin_user, created = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'placements@college.edu',
                'first_name': 'Dr. Vikram',
                'last_name': 'Mehta',
                'user_type': 'OFFICER',
                'phone_number': '+91 9876500001',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created Placement Officer / Admin: admin (password: admin123)"))

        # 2. Create Sample Students
        students_data = [
            {
                'username': 'rahul',
                'first_name': 'Rahul',
                'last_name': 'Sharma',
                'email': 'rahul.sharma@college.edu',
                'phone': '+91 9876543210',
                'roll': '21CS045',
                'dept': 'CSE',
                'year': 4,
                'cgpa': 8.75,
                'skills': 'Python, Django, PostgreSQL, Docker, Git, REST API',
                'interests': 'Backend Engineering, Cloud Software, System Design',
                'status': 'PLACED',
                'bio': 'Passionate backend developer with strong focus on high-throughput REST APIs and scalable database systems.',
            },
            {
                'username': 'priya',
                'first_name': 'Priya',
                'last_name': 'Patel',
                'email': 'priya.patel@college.edu',
                'phone': '+91 9876543211',
                'roll': '21IT023',
                'dept': 'IT',
                'year': 4,
                'cgpa': 8.40,
                'skills': 'Python, SQL, Pandas, Power BI, Tableau, Advanced Excel',
                'interests': 'Data Analytics, Business Intelligence, Data Engineering',
                'status': 'SELECTED',
                'bio': 'Data analytics enthusiast passionate about uncovering actionable business insights from big data.',
            },
            {
                'username': 'amit',
                'first_name': 'Amit',
                'last_name': 'Verma',
                'email': 'amit.verma@college.edu',
                'phone': '+91 9876543212',
                'roll': '21AI015',
                'dept': 'AI_DS',
                'year': 4,
                'cgpa': 9.15,
                'skills': 'Python, PyTorch, Scikit-Learn, TensorFlow, SQL, Docker',
                'interests': 'AI/ML Engineering, Computer Vision, Deep Learning',
                'status': 'INTERVIEWING',
                'bio': 'AI researcher and competitive coder solving complex algorithmic challenges.',
            },
            {
                'username': 'sneha',
                'first_name': 'Sneha',
                'last_name': 'Rao',
                'email': 'sneha.rao@college.edu',
                'phone': '+91 9876543213',
                'roll': '21EC088',
                'dept': 'ECE',
                'year': 4,
                'cgpa': 7.60,
                'skills': 'C++, Python, Embedded Systems, IoT, Git, Linux',
                'interests': 'Embedded Software, Firmware Engineering, Hardware IoT',
                'status': 'SHORTLISTED',
                'bio': 'Electronics engineer fascinated by IoT smart sensors and edge computing firmware.',
            },
            {
                'username': 'rohit',
                'first_name': 'Rohit',
                'last_name': 'Gupta',
                'email': 'rohit.gupta@college.edu',
                'phone': '+91 9876543214',
                'roll': '22CS012',
                'dept': 'CSE',
                'year': 3,
                'cgpa': 8.10,
                'skills': 'JavaScript, React, Node.js, Express, MongoDB, HTML5',
                'interests': 'Full Stack Web Development, Frontend Engineering',
                'status': 'APPLIED',
                'bio': 'Full-stack developer building modern user experiences with React and responsive layouts.',
            }
        ]

        created_students = {}
        for s in students_data:
            u, u_created = CustomUser.objects.get_or_create(
                username=s['username'],
                defaults={
                    'email': s['email'],
                    'first_name': s['first_name'],
                    'last_name': s['last_name'],
                    'user_type': 'STUDENT',
                    'phone_number': s['phone'],
                }
            )
            if u_created:
                u.set_password('student123')
                u.save()

            sp, sp_created = StudentProfile.objects.get_or_create(
                user=u,
                defaults={
                    'roll_number': s['roll'],
                    'full_name': f"{s['first_name']} {s['last_name']}",
                    'department': s['dept'],
                    'current_year': s['year'],
                    'cgpa': s['cgpa'],
                    'tenth_percentage': 88.5,
                    'twelfth_percentage': 86.0,
                    'skills': s['skills'],
                    'career_interests': s['interests'],
                    'placement_status': s['status'],
                    'resume_status': 'Uploaded',
                    'bio': s['bio'],
                    'linkedin_url': 'https://linkedin.com',
                    'github_url': 'https://github.com',
                }
            )
            created_students[s['username']] = sp

            # Add projects
            if sp_created:
                StudentProject.objects.create(
                    student=sp,
                    title="AI College Placement System",
                    technologies="Python, Django, SQLite, CSS3",
                    description="Full-featured campus placement management portal with AI resume scanner and automated eligibility verification.",
                    github_url="https://github.com/placement-portal"
                )
                StudentProject.objects.create(
                    student=sp,
                    title="Real-Time Data Pipeline",
                    technologies="Python, PostgreSQL, Docker",
                    description="Automated ingestion of streaming metrics with dashboard visualization."
                )
                StudentCertification.objects.create(
                    student=sp,
                    title="AWS Certified Cloud Practitioner",
                    issuing_organization="Amazon Web Services",
                    issue_date=date(2025, 8, 15)
                )

        self.stdout.write(self.style.SUCCESS(f"Verified {len(created_students)} student profiles."))

        # 3. Create Sample Companies
        companies_data = [
            {
                'name': 'Microsoft',
                'industry': 'Software & Cloud Computing',
                'type': 'PRODUCT',
                'location': 'Hyderabad / Bangalore',
                'website': 'https://www.microsoft.com',
                'email': 'campus@microsoft.com',
                'phone': '+91 80 6789 0000',
                'hr': 'Pooja Kulkarni',
                'avg_pkg': 14.5,
                'high_pkg': 18.0,
                'featured': True,
                'desc': 'Microsoft is a global technology leader empowering every person and organization on the planet to achieve more through Azure cloud, AI, and developer tools.'
            },
            {
                'name': 'Amazon',
                'industry': 'E-Commerce & Cloud Infrastructure',
                'type': 'PRODUCT',
                'location': 'Bangalore / Hyderabad / Chennai',
                'website': 'https://www.amazon.jobs',
                'email': 'university-recruiting@amazon.com',
                'phone': '+91 80 4000 5000',
                'hr': 'Karthik Raman',
                'avg_pkg': 15.0,
                'high_pkg': 18.0,
                'featured': True,
                'desc': 'Amazon is guided by four principles: customer obsession rather than competitor focus, passion for invention, commitment to operational excellence, and long-term thinking.'
            },
            {
                'name': 'TCS (Tata Consultancy Services)',
                'industry': 'Information Technology & Consulting',
                'type': 'SERVICE',
                'location': 'Pan India / Pune / Mumbai / Bangalore',
                'website': 'https://www.tcs.com',
                'email': 'campus.recruitment@tcs.com',
                'phone': '+91 22 6778 9999',
                'hr': 'Ananya Sen',
                'avg_pkg': 7.5,
                'high_pkg': 11.5,
                'featured': True,
                'desc': 'Tata Consultancy Services is an IT services, consulting and business solutions organization that has been partnering with many of the worlds largest businesses in their transformation journeys.'
            },
            {
                'name': 'Infosys',
                'industry': 'IT Services & Digital Transformation',
                'type': 'SERVICE',
                'location': 'Bangalore / Mysore / Pune / Hyderabad',
                'website': 'https://www.infosys.com',
                'email': 'talent.acquisition@infosys.com',
                'phone': '+91 80 2852 0261',
                'hr': 'Rajesh Nair',
                'avg_pkg': 7.0,
                'high_pkg': 9.5,
                'featured': True,
                'desc': 'Infosys is a global leader in next-generation digital services and consulting, enabling clients across 56 countries to navigate their digital transformation.'
            },
            {
                'name': 'Deloitte',
                'industry': 'Consulting, Analytics & Audit',
                'type': 'CONSULTING',
                'location': 'Hyderabad / Bangalore / Gurgaon',
                'website': 'https://www.deloitte.com',
                'email': 'campusindia@deloitte.com',
                'phone': '+91 40 6762 1000',
                'hr': 'Meera Desai',
                'avg_pkg': 8.8,
                'high_pkg': 12.0,
                'featured': True,
                'desc': 'Deloitte drives progress through industry-leading audit, consulting, tax, and advisory services to many of the world’s most admired brands.'
            },
            {
                'name': 'Accenture',
                'industry': 'Technology & Professional Services',
                'type': 'MNC',
                'location': 'Bangalore / Mumbai / Pune',
                'website': 'https://www.accenture.com',
                'email': 'campus.india@accenture.com',
                'phone': '+91 80 4106 0000',
                'hr': 'Siddharth Roy',
                'avg_pkg': 6.8,
                'high_pkg': 10.0,
                'featured': True,
                'desc': 'Accenture is a leading global professional services company that helps the worlds leading businesses build their digital core and optimize operations.'
            },
            {
                'name': 'Wipro',
                'industry': 'Information Technology & Consulting',
                'type': 'SERVICE',
                'location': 'Bangalore / Hyderabad / Pune',
                'website': 'https://www.wipro.com',
                'email': 'campus@wipro.com',
                'phone': '+91 80 2844 0011',
                'hr': 'Divya Pillai',
                'avg_pkg': 6.5,
                'high_pkg': 9.0,
                'featured': False,
                'desc': 'Wipro is a leading technology services and consulting company focused on building innovative solutions that address clients complex digital transformation needs.'
            },
            {
                'name': 'Capgemini',
                'industry': 'Digital Engineering & Cloud Services',
                'type': 'MNC',
                'location': 'Pune / Mumbai / Bangalore',
                'website': 'https://www.capgemini.com',
                'email': 'fresherhiring.in@capgemini.com',
                'phone': '+91 20 6699 1000',
                'hr': 'Vikas Joshi',
                'avg_pkg': 7.2,
                'high_pkg': 10.5,
                'featured': False,
                'desc': 'Capgemini is a global business and technology transformation partner, helping organizations to accelerate their transition to a digital and sustainable world.'
            },
            {
                'name': 'Cognizant',
                'industry': 'IT Services & Digital Engineering',
                'type': 'SERVICE',
                'location': 'Chennai / Bangalore / Hyderabad',
                'website': 'https://www.cognizant.com',
                'email': 'campus@cognizant.com',
                'phone': '+91 44 4209 6000',
                'hr': 'Swati Ghosh',
                'avg_pkg': 6.5,
                'high_pkg': 9.2,
                'featured': False,
                'desc': 'Cognizant engineers modern businesses, helping clients modernize technology, reimagine processes and transform experiences.'
            },
            {
                'name': 'IBM',
                'industry': 'Hybrid Cloud & Enterprise AI',
                'type': 'PRODUCT',
                'location': 'Bangalore / Hyderabad / Kochi',
                'website': 'https://www.ibm.com',
                'email': 'university.hiring@ibm.com',
                'phone': '+91 80 4068 3000',
                'hr': 'Arun Varma',
                'avg_pkg': 9.2,
                'high_pkg': 13.0,
                'featured': False,
                'desc': 'IBM combines technology and business acumen to solve the toughest client problems through Red Hat hybrid cloud and watsonx enterprise AI.'
            }
        ]

        created_companies = {}
        for c in companies_data:
            comp, _ = Company.objects.get_or_create(
                name=c['name'],
                defaults={
                    'industry': c['industry'],
                    'company_type': c['type'],
                    'location': c['location'],
                    'website': c['website'],
                    'contact_email': c['email'],
                    'contact_phone': c['phone'],
                    'hr_name': c['hr'],
                    'average_package': c['avg_pkg'],
                    'highest_package': c['high_pkg'],
                    'is_featured': c['featured'],
                    'description': c['desc'],
                }
            )
            created_companies[c['name']] = comp

        self.stdout.write(self.style.SUCCESS(f"Verified {len(created_companies)} companies."))

        # 4. Create Sample Placement Drives / Jobs
        today = timezone.now().date()
        drives_data = [
            {
                'company': 'Microsoft',
                'title': 'Software Development Engineer - I',
                'type': 'FULL_TIME',
                'location': 'Hyderabad / Bangalore',
                'package': 18.0,
                'cgpa': 7.5,
                'backlogs': 0,
                'depts': 'CSE,IT,AI_DS,ECE',
                'years': '4',
                'skills': 'Data Structures, Algorithms, C++, Python, System Design',
                'vacancies': 12,
                'deadline': today + timedelta(days=14),
                'drive_date': today + timedelta(days=20),
                'desc': 'Join Azure Cloud or Developer Tools engineering teams. You will design, build and test large-scale distributed cloud systems handling millions of queries per second.',
                'process': '1. Online Assessment (2 DSA Coding Problems)\n2. Technical Round 1 (Problem Solving & Algorithms)\n3. Technical Round 2 (System Design & Code Quality)\n4. AA / HR Discussion',
            },
            {
                'company': 'Amazon',
                'title': 'Associate Software Developer',
                'type': 'FULL_TIME',
                'location': 'Bangalore',
                'package': 16.5,
                'cgpa': 7.5,
                'backlogs': 0,
                'depts': 'CSE,IT,AI_DS,ECE,EEE',
                'years': '4',
                'skills': 'Java, Python, OOP, SQL, Problem Solving',
                'vacancies': 15,
                'deadline': today + timedelta(days=12),
                'drive_date': today + timedelta(days=18),
                'desc': 'Build high-scale systems that power e-commerce and AWS services worldwide. Looking for candidates with strong foundational algorithmic thinking.',
                'process': '1. Online Code Assessment\n2. Technical Coding Round\n3. System Architecture Round\n4. Bar Raiser HR Interview',
            },
            {
                'company': 'TCS (Tata Consultancy Services)',
                'title': 'Python / Django Developer (TCS Digital)',
                'type': 'FULL_TIME',
                'location': 'Pan India / Pune',
                'package': 7.5,
                'cgpa': 6.5,
                'backlogs': 0,
                'depts': 'CSE,IT,AI_DS,ECE,EEE,MECH,CIVIL,MCA',
                'years': '3,4',
                'skills': 'Python, Django, SQL, REST API, Git',
                'vacancies': 40,
                'deadline': today + timedelta(days=8),
                'drive_date': today + timedelta(days=15),
                'desc': 'Develop enterprise web applications, REST microservices, and automated backend data processing pipelines for Fortune 500 financial clients.',
                'process': '1. TCS NQT Online Test\n2. Technical Coding Interview\n3. Managerial & HR Interview',
            },
            {
                'company': 'Deloitte',
                'title': 'Data Analyst / Consultant',
                'type': 'FULL_TIME',
                'location': 'Hyderabad / Bangalore',
                'package': 8.8,
                'cgpa': 7.0,
                'backlogs': 0,
                'depts': 'CSE,IT,AI_DS,ECE,MCA,MBA',
                'years': '4',
                'skills': 'SQL, Python, Power BI, Advanced Excel, Statistics',
                'vacancies': 20,
                'deadline': today + timedelta(days=10),
                'drive_date': today + timedelta(days=16),
                'desc': 'Analyze operational and marketing data, build executive dashboards in Power BI, and present data-driven recommendations to multinational clients.',
                'process': '1. Aptitude & Verbal Assessment\n2. Case Study Evaluation\n3. Partner Interview Round',
            },
            {
                'company': 'IBM',
                'title': 'Data Engineer - Cloud & AI',
                'type': 'FULL_TIME',
                'location': 'Bangalore / Remote',
                'package': 9.2,
                'cgpa': 7.0,
                'backlogs': 0,
                'depts': 'CSE,IT,AI_DS,ECE',
                'years': '4',
                'skills': 'Python, SQL, Apache Spark, Airflow, Docker',
                'vacancies': 10,
                'deadline': today + timedelta(days=15),
                'drive_date': today + timedelta(days=22),
                'desc': 'Design and implement scalable ETL and streaming data pipelines connecting hybrid enterprise clouds with watsonx AI models.',
                'process': '1. Coding & SQL Assessment\n2. Technical Architecture Round\n3. HR Cultural Interview',
            },
            {
                'company': 'Accenture',
                'title': 'Full Stack Web Developer',
                'type': 'FULL_TIME',
                'location': 'Bangalore / Pune',
                'package': 6.8,
                'cgpa': 6.5,
                'backlogs': 1,
                'depts': 'CSE,IT,AI_DS,ECE,EEE,MCA',
                'years': '3,4',
                'skills': 'JavaScript, React, Python, HTML5, CSS3, SQL',
                'vacancies': 30,
                'deadline': today + timedelta(days=20),
                'drive_date': today + timedelta(days=26),
                'desc': 'Build responsive modern user portals, integrate backend APIs, and collaborate in agile engineering sprints across global teams.',
                'process': '1. Cognitive & Technical Assessment\n2. Coding Assessment\n3. Virtual Interview',
            }
        ]

        created_drives = []
        for d in drives_data:
            comp = created_companies.get(d['company'])
            if not comp:
                continue
            drive, _ = PlacementDrive.objects.get_or_create(
                company=comp,
                title=d['title'],
                defaults={
                    'job_type': d['type'],
                    'experience_required': d.get('experience', '1_TO_3_YEARS'),
                    'location': d['location'],
                    'salary_package': d['package'],
                    'minimum_cgpa': d['cgpa'],
                    'max_backlogs': d['backlogs'],
                    'eligible_departments': d['depts'],
                    'eligible_years': d['years'],
                    'required_skills': d['skills'],
                    'vacancies': d['vacancies'],
                    'application_deadline': d['deadline'],
                    'drive_date': d['drive_date'],
                    'description': d['desc'],
                    'selection_process': d['process'],
                    'is_active': True,
                }
            )
            created_drives.append(drive)

        self.stdout.write(self.style.SUCCESS(f"Verified {len(created_drives)} active placement drives."))

        # 5. Create Sample Applications, Interviews, and Offers
        if created_drives and 'rahul' in created_students:
            # Rahul applied to Microsoft, TCS
            rahul = created_students['rahul']
            ms_drive = next((d for d in created_drives if d.company.name == 'Microsoft'), None)
            if ms_drive:
                app, _ = JobApplication.objects.get_or_create(
                    student=rahul,
                    job=ms_drive,
                    defaults={'status': 'SELECTED', 'notes': 'Exceptional problem solving performance in algorithms.'}
                )
                PlacementOffer.objects.get_or_create(
                    application=app,
                    defaults={
                        'job_role': 'Software Development Engineer - I',
                        'package_offered': 18.0,
                        'selection_date': today - timedelta(days=5),
                    }
                )

            tcs_drive = next((d for d in created_drives if 'TCS' in d.company.name), None)
            if tcs_drive:
                JobApplication.objects.get_or_create(
                    student=rahul,
                    job=tcs_drive,
                    defaults={'status': 'SELECTED'}
                )

        if created_drives and 'priya' in created_students:
            priya = created_students['priya']
            deloitte_drive = next((d for d in created_drives if d.company.name == 'Deloitte'), None)
            if deloitte_drive:
                app, _ = JobApplication.objects.get_or_create(
                    student=priya,
                    job=deloitte_drive,
                    defaults={'status': 'SELECTED'}
                )
                PlacementOffer.objects.get_or_create(
                    application=app,
                    defaults={
                        'job_role': 'Data Analyst / Consultant',
                        'package_offered': 8.8,
                        'selection_date': today - timedelta(days=2),
                    }
                )

        if created_drives and 'amit' in created_students:
            amit = created_students['amit']
            ibm_drive = next((d for d in created_drives if d.company.name == 'IBM'), None)
            if ibm_drive:
                app, _ = JobApplication.objects.get_or_create(
                    student=amit,
                    job=ibm_drive,
                    defaults={'status': 'TECHNICAL_INTERVIEW'}
                )
                InterviewSchedule.objects.get_or_create(
                    application=app,
                    defaults={
                        'title': 'Technical Round 1: Data Architectures',
                        'interview_type': 'TECHNICAL_INTERVIEW',
                        'interview_date': today + timedelta(days=3),
                        'interview_time': time(11, 30),
                        'location_or_link': 'Campus Placement Cell Room 302 / Webex',
                        'interviewer_notes': 'Be prepared to explain Spark partitions and schema design.',
                    }
                )

        # 6. Create Announcements
        announcements_data = [
            {
                'title': 'Microsoft SDE Campus Drive Announced for 2026 Batch',
                'category': 'DRIVE',
                'content': 'Microsoft India has formally confirmed on-campus recruitment for Software Development Engineer roles offering ₹18.0 LPA CTC. All CSE, IT, and AI & DS students with CGPA >= 7.5 are advised to complete their profile and apply before the deadline.',
                'pinned': True,
            },
            {
                'title': 'Aptitude & Technical Coding Mock Assessment',
                'category': 'TEST',
                'content': 'An institutional mock placement test will be conducted online this Saturday from 10:00 AM to 12:30 PM. Use the AI Interview Preparation module to practice preceding rounds.',
                'pinned': True,
            },
            {
                'title': 'TCS Digital Drive Schedule & Venue Guidelines',
                'category': 'INTERVIEW',
                'content': 'Shortlisted candidates for TCS Digital Technical Interviews should report in formal collegiate attire with 2 hard copies of their placement resume and College ID proof.',
                'pinned': False,
            }
        ]

        for ann in announcements_data:
            Announcement.objects.get_or_create(
                title=ann['title'],
                defaults={
                    'category': ann['category'],
                    'content': ann['content'],
                    'is_pinned': ann['pinned'],
                }
            )

        self.stdout.write(self.style.SUCCESS("All sample data seeded successfully!"))
