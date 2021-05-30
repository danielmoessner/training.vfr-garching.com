from django import forms
from django.contrib import admin
from apps.settings.models import General, Trainings, Fundamentals
from solo.admin import SingletonModelAdmin


class GeneralForm(forms.ModelForm):
    class Meta:
        model = General
        fields = '__all__'
        widgets = {
            'meta_description': forms.Textarea
        }


class GeneralAdmin(SingletonModelAdmin):
    form = GeneralForm


admin.site.register(General, GeneralAdmin)
admin.site.register(Trainings, SingletonModelAdmin)
admin.site.register(Fundamentals, SingletonModelAdmin)
