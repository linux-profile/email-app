from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from django.views.generic import View, FormView
from django.conf import settings

from modules.account.utils import (
    send_activation_email,
)
from modules.account.forms import (
    ResendActivationCodeForm,
    ResendActivationCodeViaEmailForm,
)
from modules.account.models import Activation
from core.views import GuestOnlyView


class ResendActivationCodeView(GuestOnlyView, FormView):
    template_name = 'account/resend_activation_code.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME:
            return ResendActivationCodeViaEmailForm

        return ResendActivationCodeForm

    def form_valid(self, form):
        user = form.user_cache

        activation = user.activation_set.first()
        activation.delete()

        code = get_random_string(20)

        act = Activation()
        act.code = code
        act.user = user
        act.save()

        send_activation_email(self.request, user.email, code)

        messages.success(self.request, _('A new activation code has been sent to your email address.'))

        return redirect('account:resend_activation_code')


class ActivateView(View):

    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Activate profile
        user = act.user
        user.is_active = True
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('You have successfully activated your account!'))

        return redirect('account:log_in')
