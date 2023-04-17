from django.urls import path

from modules.account.management.views import (
    ChangeEmailView,
    ChangeEmailActivateView,
    ChangeProfileView,
    ChangePasswordView
)


urlpatterns = [
    path('email/', ChangeEmailView.as_view(), name='change_email'),
    path('email/<code>/', ChangeEmailActivateView.as_view(), name='change_email_activation'),
    path('profile/', ChangeProfileView.as_view(), name='change_profile'),
    path('password/', ChangePasswordView.as_view(), name='change_password'),
]
