from .models import Training
from django import forms


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'x-model': field}


class Step1Form(forms.ModelForm):
    name = forms.CharField(label='Text', widget=forms.TextInput(attrs={'x-model': 'name'}))

    class Meta:
        model = Training
        fields = ['name', 'topic', 'structure']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'x-model': field}


class Step2Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['name', 'topic', 'structure', 'exercise1', 'exercise2', 'exercise3', 'exercise4', 'exercise5']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].required = True
        self.fields['structure'].required = True
