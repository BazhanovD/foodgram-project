from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='registration/changePassword.html'), ),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/changePasswordDone.html'), ),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/resetPassword.html'), ),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/resetPasswordDone.html'), ),
    path('reset/<slug:uidb64>/<slug:token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/renewPassword.html'), ),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/renewPasswordDone.html'), ),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='registration/logout.html'), ),
]
