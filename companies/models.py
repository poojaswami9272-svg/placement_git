from django.db import models

COMPANY_TYPE_CHOICES = (
    ('PRODUCT', 'Product Based'),
    ('SERVICE', 'Service Based'),
    ('STARTUP', 'Startup'),
    ('MNC', 'Multinational Corporation'),
    ('CONSULTING', 'Consulting & Analytics'),
    ('FINTECH', 'FinTech & Banking'),
)

class Company(models.Model):
    name = models.CharField(max_length=150, unique=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    description = models.TextField()
    industry = models.CharField(max_length=100, default='Information Technology')
    company_type = models.CharField(max_length=30, choices=COMPANY_TYPE_CHOICES, default='PRODUCT')
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=150, default='Pan India / Remote')
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=30, blank=True, null=True)
    hr_name = models.CharField(max_length=100, blank=True, null=True)
    average_package = models.DecimalField(max_digits=5, decimal_places=2, default=6.50, help_text="In LPA (Lakhs Per Annum)")
    highest_package = models.DecimalField(max_digits=5, decimal_places=2, default=12.00, help_text="In LPA")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def total_drives_count(self):
        return self.placement_drives.count()

    @property
    def total_selections_count(self):
        return self.placement_drives.filter(applications__status__in=['SELECTED', 'PLACED']).count()
