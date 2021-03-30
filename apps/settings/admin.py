from django.contrib import admin
from apps.settings.models import General
from solo.admin import SingletonModelAdmin

admin.site.register(General, SingletonModelAdmin)
