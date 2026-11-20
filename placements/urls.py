from django.urls import path
from . import views

urlpatterns = [
    path('', views.drive_list_view, name='drive_list'),
    path('add/', views.drive_create_view, name='drive_create'),
    path('<int:drive_id>/', views.drive_detail_view, name='drive_detail'),
    path('<int:drive_id>/edit/', views.drive_edit_view, name='drive_edit'),
    path('<int:drive_id>/delete/', views.drive_delete_view, name='drive_delete'),
    path('<int:drive_id>/check-eligibility/', views.check_eligibility_ajax, name='check_eligibility'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('announcements/', views.announcements_view, name='announcements'),
]
