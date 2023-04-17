from django.urls import path

from modules.account.security.views import (
    RemindUsernameView,
    RestorePasswordView,
    RestorePasswordDoneView,
    RestorePasswordConfirmView,
)


urlpatterns = [
    path('username/', RemindUsernameView.as_view(), name='remind_username'),
    path('password/', RestorePasswordView.as_view(), name='restore_password'),
    path('password/done/', RestorePasswordDoneView.as_view(), name='restore_password_done'),
    path('password/<uidb64>/<token>/', RestorePasswordConfirmView.as_view(), name='restore_password_confirm'),
]
