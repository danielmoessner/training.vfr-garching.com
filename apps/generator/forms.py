from apps.trainings.models import Training
from django import forms


class Step1Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['topic']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'x-model': field}


class Step2Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['structure']

    def __init__(self, topic=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if topic:
            self.fields['structure'].queryset = topic.structures.all()
        for field in self.fields:
            self.fields[field].widget.attrs = {'x-model': field}


class Step3Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['block1', 'block2', 'block3', 'block4', 'block5']

    def __init__(self, structure=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if structure:
            for i in range(1, 6):
                self.fields['block{}'.format(i)].queryset = getattr(structure, 'blocks{}'.format(i)).all()
        for field in self.fields:
            self.fields[field].widget.attrs = {'x-model': field}
