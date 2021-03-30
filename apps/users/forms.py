from django import forms
from apps.trainings.models import AgeGroup
from apps.users.models import UserSettings


class SelectAgeGroupForm(forms.ModelForm):
    age_group = forms.ModelChoiceField(queryset=AgeGroup.objects.all(), widget=forms.RadioSelect, required=False)

    class Meta:
        model = UserSettings
        fields = ('age_group', )
