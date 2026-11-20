from django.urls import path
from . import views

urlpatterns = [
    path('', views.company_list_view, name='company_list'),
    path('add/', views.company_create_view, name='company_create'),
    path('<int:company_id>/', views.company_detail_view, name='company_detail'),
    path('<int:company_id>/edit/', views.company_edit_view, name='company_edit'),
    path('<int:company_id>/delete/', views.company_delete_view, name='company_delete'),
]
