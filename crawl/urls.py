from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log/', views.log_drink, name='log_drink'),
    path('profile/', views.profile, name='profile'),
    path('admin-view/', views.admin_view, name='admin_view'),
    path('login/<uuid:token>/', views.qr_login, name='qr_login'),
    path('', views.landing_page, name='landing_page'),  # Landing page for non-logged-in users
    path('feed/', views.feed, name='feed'),
    path('delete_drink/<int:drink_id>/', views.delete_drink, name='delete_drink'),  # New URL pattern
    path('post-status/', views.post_status, name='post_status'),
    path('delete-status/<int:status_id>/', views.delete_status, name='delete_status'),
    path('map/', views.map, name='map'),
]

handler404 = 'crawl.views.custom_404'  # Ensure this view exists
