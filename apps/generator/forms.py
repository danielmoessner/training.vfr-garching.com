from apps.generator.models import Topic, Structure
from apps.trainings.models import Training
from django import forms


class Step1Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'topic':
                self.fields[field].widget = forms.HiddenInput()
            self.fields[field].widget.attrs = {'x-model': field}


class Step2Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'

    def __init__(self, initial=None, *args, **kwargs):
        super().__init__(initial=initial, *args, **kwargs)
        if initial and 'topic' in initial and initial['topic'] != ['']:
            initial['topic'] = initial['topic'][0]
            topic = Topic.objects.get(pk=initial['topic'])
            self.fields['structure'].queryset = topic.structures.all()
        for field in self.fields:
            if field != 'structure':
                self.fields[field].widget = forms.HiddenInput()
            self.fields[field].widget.attrs = {'x-model': field}
        self.fields['topic'].widget = forms.HiddenInput()


class Step3Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'

    def __init__(self, initial=None, *args, **kwargs):
        super().__init__(initial=initial, *args, **kwargs)
        if initial and 'structure' in initial and initial['structure'] != ['']:
            structure = Structure.objects.get(pk__in=initial['structure'])
            for i in range(1, 6):
                self.fields['block{}'.format(i)].queryset = getattr(structure, 'blocks{}'.format(i)).all()
                self.fields['block{}'.format(i)].empty_label = None
            if not structure.phase5:
                self.fields['block5'].widget = forms.HiddenInput()
        for field in self.fields:
            if field[:5] != 'block':
                self.fields[field].widget = forms.HiddenInput()
            self.fields[field].widget.attrs = {'x-model': field}
        self.fields['topic'].widget = forms.HiddenInput()
        self.fields['structure'].widget = forms.HiddenInput()


class Step4Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
            self.fields[field].widget = forms.HiddenInput()
            self.fields[field].widget.attrs = {'x-model': field}


class Step5Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'name':
                self.fields[field].widget = forms.HiddenInput()
            self.fields[field].widget.attrs = {'x-model': field}


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'
