from .models import Training
from django import forms


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'


class Step1Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['name', 'topic', 'structure']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].required = True
        self.fields['structure'].required = True


class Step2Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['name', 'topic', 'structure', 'exercise1', 'exercise2', 'exercise3', 'exercise4', 'exercise5']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].required = True
        self.fields['structure'].required = True
