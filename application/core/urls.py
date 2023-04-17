from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from modules.dashboard.views import DashboardPageView, ChangeLanguageView

urlpatterns = [
    path('', DashboardPageView.as_view(), name='index'),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('account/', include('modules.account.urls')),
    path('backoffice/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
