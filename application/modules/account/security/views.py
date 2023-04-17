from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    PasswordResetDoneView as BasePasswordResetDoneView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.shortcuts import redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from django.views.generic import FormView
from django.conf import settings

from modules.account.utils import (
    send_reset_password_email,
    send_forgotten_username_email,
)
from modules.account.security.forms import (
    RestorePasswordForm,
    RestorePasswordViaEmailOrUsernameForm,
    RemindUsernameForm,
)
from core.views import GuestOnlyView


class RestorePasswordView(GuestOnlyView, FormView):
    template_name = 'account/security/restore_password.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME:
            return RestorePasswordViaEmailOrUsernameForm

        return RestorePasswordForm

    def form_valid(self, form):
        user = form.user_cache
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        if isinstance(uid, bytes):
            uid = uid.decode()

        send_reset_password_email(self.request, user.email, token, uid)

        return redirect('account:restore_password_done')


class RestorePasswordDoneView(BasePasswordResetDoneView):
    template_name = 'account/security/restore_password_done.html'


class RestorePasswordConfirmView(BasePasswordResetConfirmView):
    template_name = 'account/security/restore_password_confirm.html'

    def form_valid(self, form):
        # Change the password
        form.save()

        messages.success(self.request, _('Your password has been set. You may go ahead and log in now.'))

        return redirect('account:log_in')


class RemindUsernameView(GuestOnlyView, FormView):
    template_name = 'account/security/remind_username.html'
    form_class = RemindUsernameForm

    def form_valid(self, form):
        user = form.user_cache
        send_forgotten_username_email(user.email, user.username)

        messages.success(self.request, _('Your username has been successfully sent to your email.'))

        return redirect('account:remind_username')
