from django.urls import path
from account.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePassword,SentPasswordResetEmailView, PasswordResetView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name= 'register'),
    path('login/', UserLoginView.as_view(), name= 'login'),
    path('profile/', UserProfileView.as_view(), name= 'profile'),
    path('change-Password/', UserChangePassword.as_view(), name= 'changePassowrd'),
    path('send-reset-password-email/', SentPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', PasswordResetView.as_view(), name='reset-password'),
]