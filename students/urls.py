from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.student_profile_view, name='student_profile'),
    path('profile/edit/', views.student_edit_profile_view, name='edit_student_profile'),
    path('resume/', views.resume_management_view, name='my_resume'),
    path('documents/', views.documents_management_view, name='documents'),
    path('projects/add/', views.add_project_view, name='add_project'),
    path('projects/<int:project_id>/delete/', views.delete_project_view, name='delete_project'),
    path('certifications/add/', views.add_certification_view, name='add_certification'),
    path('certifications/<int:cert_id>/delete/', views.delete_certification_view, name='delete_certification'),
    path('', views.student_list_view, name='student_list_root'),
    path('all/', views.student_list_view, name='student_list'),
    path('<int:student_id>/', views.student_detail_view, name='student_detail'),
]
