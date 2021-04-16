from django import forms
from apps.trainings.models import Youth, Difficulty
from apps.users.models import UserSettings


class SelectAgeGroupForm(forms.ModelForm):
    age_group = forms.ModelChoiceField(queryset=Youth.objects.all(), widget=forms.RadioSelect, required=False)

    class Meta:
        model = UserSettings
        fields = ('age_group',)


class SelectDifficultiesForm(forms.ModelForm):
    difficulties = forms.ModelMultipleChoiceField(queryset=Difficulty.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = UserSettings
        fields = ('difficulties',)


class SearchForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ('search', )
