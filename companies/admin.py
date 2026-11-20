from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'company_type', 'location', 'average_package', 'highest_package', 'is_featured')
    list_filter = ('company_type', 'industry', 'is_featured')
    search_fields = ('name', 'description', 'location', 'hr_name')
