from django import forms
from django.conf import settings
from django.contrib import admin
from apps.settings.models import General, Trainings, Fundamentals
from solo.admin import SingletonModelAdmin
from tinymce.widgets import TinyMCE


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

attrs = settings.TINYMCE_DEFAULT_CONFIG.update({
    "toolbar": "undo redo | formatselect | "
               "bold italic underline | forecolor backcolor | alignleft aligncenter "
               "alignright alignjustify | bullist numlist | outdent indent | media",
})


class FundamentalsForm(forms.ModelForm):
    class Meta:
        model = Fundamentals
        fields = '__all__'
        widgets = {
            'content': TinyMCE(attrs=attrs)
        }


class FundamentalsAdmin(SingletonModelAdmin):
    form = FundamentalsForm


admin.site.register(Fundamentals, FundamentalsAdmin)
