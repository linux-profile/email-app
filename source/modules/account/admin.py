from django.contrib import admin
from core.utils import get_field_list
from modules.account.models import Activation


class ProductAdmin(admin.ModelAdmin):
    list_display = get_field_list(Activation)


admin.site.register(Activation, ProductAdmin)
