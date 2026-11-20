from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_assistant_chat_view, name='ai_assistant_root'),
    path('chat/', views.ai_assistant_chat_view, name='ai_assistant'),
    path('assistant/', views.ai_assistant_chat_view, name='ai_assistant_alias'),
    path('resume-analyzer/', views.ai_resume_analyzer_view, name='ai_resume_analyzer'),
    path('jd-analyzer/', views.ai_jd_analyzer_view, name='ai_jd_analyzer'),
    path('interview-prep/', views.ai_interview_prep_view, name='ai_interview_prep'),
    path('career-roadmap/', views.ai_career_roadmap_view, name='ai_career_roadmap'),
]
