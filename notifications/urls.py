from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list_view, name='notifications'),
    path('<int:notif_id>/read/', views.mark_notification_read_view, name='mark_notification_read'),
]
