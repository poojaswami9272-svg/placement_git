import os
from django.core.management.base import BaseCommand
from django.conf import settings
from companies.models import Company
from students.models import StudentProfile
from placements.models import PlacementDrive

class Command(BaseCommand):
    help = "Generate SVGs for companies and connect all generated images to database models"

    def handle(self, *args, **kwargs):
        static_logos = settings.BASE_DIR / 'static' / 'images' / 'companies'
        media_logos = settings.MEDIA_ROOT / 'company_logos'
        os.makedirs(static_logos, exist_ok=True)
        os.makedirs(media_logos, exist_ok=True)

        companies_svg = {
            'Microsoft': ('microsoft.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="5" y="5" width="42" height="42" fill="#F25022"/><rect x="53" y="5" width="42" height="42" fill="#7FBA00"/><rect x="5" y="53" width="42" height="42" fill="#00A4EF"/><rect x="53" y="53" width="42" height="42" fill="#FFB900"/></svg>'),
            'Amazon': ('amazon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#131921"/><text x="50" y="46" fill="#FFFFFF" font-size="24" font-weight="bold" font-family="Arial" text-anchor="middle">amazon</text><path d="M22 66 Q50 82 78 66" fill="none" stroke="#FF9900" stroke-width="5" stroke-linecap="round"/><polygon points="75,62 82,67 78,72" fill="#FF9900"/></svg>'),
            'TCS': ('tcs.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#001C3D"/><text x="50" y="58" fill="#00B4D8" font-size="32" font-weight="900" font-family="Arial" text-anchor="middle">TCS</text></svg>'),
            'Infosys': ('infosys.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#007CC3"/><text x="50" y="58" fill="#FFFFFF" font-size="22" font-weight="bold" font-family="Arial" text-anchor="middle">Infosys</text></svg>'),
            'Deloitte': ('deloitte.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#000000"/><text x="42" y="58" fill="#FFFFFF" font-size="18" font-weight="bold" font-family="Arial" text-anchor="middle">Deloitte</text><circle cx="84" cy="56" r="4" fill="#86BC25"/></svg>'),
            'IBM': ('ibm.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#0F62FE"/><text x="50" y="60" fill="#FFFFFF" font-size="30" font-weight="900" font-family="Arial" text-anchor="middle" letter-spacing="2">IBM</text></svg>'),
            'Accenture': ('accenture.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#A100FF"/><text x="46" y="58" fill="#FFFFFF" font-size="16" font-weight="bold" font-family="Arial" text-anchor="middle">accenture</text><text x="84" y="46" fill="#FFFFFF" font-size="20" font-weight="bold" font-family="Arial">&gt;</text></svg>'),
            'Wipro': ('wipro.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="2"/><circle cx="35" cy="35" r="12" fill="#E53935"/><circle cx="65" cy="35" r="12" fill="#1E88E5"/><circle cx="35" cy="65" r="12" fill="#43A047"/><circle cx="65" cy="65" r="12" fill="#FB8C00"/></svg>'),
            'Capgemini': ('capgemini.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#0070AD"/><text x="50" y="58" fill="#FFFFFF" font-size="15" font-weight="bold" font-family="Arial" text-anchor="middle">Capgemini</text></svg>'),
            'Cognizant': ('cognizant.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="#0033A0"/><text x="50" y="58" fill="#FFFFFF" font-size="16" font-weight="bold" font-family="Arial" text-anchor="middle">cognizant</text></svg>'),
        }

        for comp_key, (filename, svg_code) in companies_svg.items():
            # Write to static and media
            (static_logos / filename).write_text(svg_code, encoding='utf-8')
            (media_logos / filename).write_text(svg_code, encoding='utf-8')

            # Update database Company model with logo path
            Company.objects.filter(name__icontains=comp_key).update(logo=f'company_logos/{filename}')

        # Connect student profile photos
        StudentProfile.objects.filter(user__username='rahul').update(profile_photo='student_photos/student_rahul.jpg')
        StudentProfile.objects.filter(user__username='priya').update(profile_photo='student_photos/student_priya.jpg')
        StudentProfile.objects.filter(user__username='amit').update(profile_photo='student_photos/student_rahul.jpg')
        StudentProfile.objects.filter(user__username='sneha').update(profile_photo='student_photos/student_priya.jpg')

        # Connect job drive banners
        PlacementDrive.objects.filter(company__name__icontains='Microsoft').update(banner_image='job_banners/hero_students.jpg')
        PlacementDrive.objects.filter(company__name__icontains='Amazon').update(banner_image='job_banners/hero_students.jpg')

        self.stdout.write(self.style.SUCCESS("All SVG logos created and image assets connected to database!"))
