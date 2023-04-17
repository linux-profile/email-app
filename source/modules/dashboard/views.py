from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardPageView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'


class ChangeLanguageView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/change_language.html'
