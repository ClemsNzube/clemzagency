from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('lease/', views.lease_property, name='lease_property'),
    path('property/<int:property_id>/rent/', views.rent_property, name='rent_property'),
    path('rent/success/', views.rent_success, name='rent_success'),
    path('properties/', views.property_list, name='property_list'),
    path('payment/callback/', views.paystack_callback, name='paystack_callback'),
    path('paystack_payment/<int:property_id>/', views.paystack_payment, name='paystack_payment'),
]
