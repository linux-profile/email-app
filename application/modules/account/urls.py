from django.urls import path, include

from modules.account.views import (
    LogInView,
    LogOutView,
    SignUpView,
)

app_name = 'account'

urlpatterns = [
    path('log-in/', LogInView.as_view(), name='log_in'),
    path('log-out/', LogOutView.as_view(), name='log_out'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),

    path('security/', include('modules.account.security.urls')),
    path('management/', include('modules.account.management.urls')),
    path('status/', include('modules.account.status.urls')),
]
