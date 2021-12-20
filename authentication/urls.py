from django.urls import path
from .views import RegisterView, VarifyEmail, LoginApiView, PasswordTokenCheckApiView, PasswordResetPasswordApiView, \
    SetNewPasswordApiView, LogoutApiView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/', VarifyEmail.as_view(), name='email-verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('password-reset/', PasswordResetPasswordApiView.as_view(), name='password-reset'),
    path('password-reset-token/<uuid64>/<token>/', PasswordTokenCheckApiView.as_view(), name='password-reset-token'),
    path('password-reset-complete/', SetNewPasswordApiView.as_view(), name='password-reset-complete'),
]
