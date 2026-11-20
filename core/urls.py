from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('statistics/', views.placement_statistics_view, name='placement_statistics'),
    path('contact/', views.contact_view, name='contact'),
    path('reports/', views.reports_view, name='reports'),
    path('reports/export/students/excel/', views.export_students_excel, name='export_students_excel'),
    path('reports/export/companies/excel/', views.export_companies_excel, name='export_companies_excel'),
    path('reports/export/placements/pdf/', views.export_placements_pdf, name='export_placements_pdf'),
]
