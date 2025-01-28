from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('', views.home, name='home'),  # Maps the root URL to the home view
    path('dashboard/', views.dashboard, name='dashboard'),  # Maps the /dashboard/ URL to the dashboard view
    path('property/', views.property, name='property'),  # Maps the /property/ URL to the property view
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('agents/', views.agent_list, name='agent_list'),
    path('dashboard/property/<int:property_id>/', views.dashboard_property_detail, name='lease_detail'),
]
