from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='changePassword.html'), ),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='changePasswordDone.html'), ),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='resetPassword.html'), ),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='resetPasswordDone.html'), ),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='renewPassword.html'), ),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='renewPasswordDone.html'), ),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='logout.html'), ),
]
