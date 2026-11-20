from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:drive_id>/', views.apply_job_view, name='apply_job'),
    path('my/', views.my_applications_view, name='my_applications'),
    path('officer/', views.officer_applications_view, name='officer_applications'),
    path('<int:application_id>/status/', views.update_application_status_view, name='update_application_status'),
    path('<int:application_id>/schedule-interview/', views.schedule_interview_view, name='schedule_interview'),
    path('<int:application_id>/record-selection/', views.record_selection_view, name='record_selection'),
]
