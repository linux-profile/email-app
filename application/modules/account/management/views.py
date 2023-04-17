from django.contrib import messages
from django.contrib.auth import login

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView as BasePasswordChangeView,
)
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from django.views.generic import View, FormView
from django.conf import settings

from modules.account.utils import (
    send_activation_change_email
)
from modules.account.forms import (
    ChangeProfileForm,
    ChangeEmailForm,
)
from modules.account.models import Activation


class ChangeEmailView(LoginRequiredMixin, FormView):
    template_name = 'account/management/change_email.html'
    form_class = ChangeEmailForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        user = self.request.user
        email = form.cleaned_data['email']

        if settings.ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.email = email
            act.save()

            send_activation_change_email(self.request, email, code)

            messages.success(self.request, _('To complete the change of email address, click on the link sent to it.'))
        else:
            user.email = email
            user.save()

            messages.success(self.request, _('Email successfully changed.'))

        return redirect('account:change_email')


class ChangeEmailActivateView(View):

    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Change the email
        user = act.user
        user.email = act.email
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('You have successfully changed your email!'))

        return redirect('account:change_email')


class ChangeProfileView(LoginRequiredMixin, FormView):
    template_name = 'account/management/change_profile.html'
    form_class = ChangeProfileForm

    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        messages.success(self.request, _('Profile data has been successfully updated.'))

        return redirect('account:change_profile')
    

class ChangePasswordView(BasePasswordChangeView):
    template_name = 'account/management/change_password.html'

    def form_valid(self, form):
        # Change the password
        user = form.save()

        # Re-authentication
        login(self.request, user)

        messages.success(self.request, _('Your password was changed.'))

        return redirect('account:change_password')
