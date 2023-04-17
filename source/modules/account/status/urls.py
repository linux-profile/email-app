from django.urls import path

from modules.account.status.views import (
    ResendActivationCodeView,
    ActivateView,
)


urlpatterns = [
    path('resend/activation-code/', ResendActivationCodeView.as_view(), name='resend_activation_code'),
    path('activate/<code>/', ActivateView.as_view(), name='activate'),
]
