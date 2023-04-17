from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import View


class GuestOnlyView(View):
    """Redirect to the index page if the user already authenticated.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class UserCacheMixin:
    user_cache = None
