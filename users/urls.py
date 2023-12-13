from django.urls import path, include
from . import views
from .views import LogoutView
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import reverse_lazy

app_name = 'users'

urlpatterns = [
    path('auth/login', auth_views.LoginView.as_view(template_name = 'registration/login.html'), name = 'login'),
    path('auth/register', views.register, name = 'register'),
    path('logout', LogoutView.as_view(), name = 'logout'),
    path('profile', views.profile, name = 'profile'),
    path('password-reset',
        auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset.html",
        success_url = reverse_lazy('users:password_reset_done')),
        name = "password_reset"),
    path('password-reset-sent',
        auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_sent.html"),
        name = "password_reset_done"),
    path('reset/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html",
        success_url = reverse_lazy('users:password_reset_complete')),
        name="password_reset_confirm"),
    path('password-reset-complete',
        auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_done.html"),   
        name="password_reset_complete"),
]