from django.urls import path

from django.urls import path

from api.views import UserRegistrationAPI, UserLoginAPI, EmailVerifyAPI, PasswordResetAPI, PasswordResetConfirmAPI,DailyCheckinAPI

urlpatterns = [
    path('register/', UserRegistrationAPI.as_view(), name='register'),
    path('login/', UserLoginAPI.as_view(), name='login'),
    path('verify/', EmailVerifyAPI.as_view(), name='email-verify'),
    path('reset-link/', PasswordResetAPI.as_view(), name='password-reset-link'),
    path('reset-password/', PasswordResetConfirmAPI.as_view(), name='password-reset'),
    path('check-in/',DailyCheckinAPI.as_view(), name='check-in')
]
