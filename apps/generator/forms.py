from django.utils.safestring import mark_safe
from apps.generator.models import Topic, Structure, Training
from django import forms


class Step1Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'

    def __init__(self, settings=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].label = mark_safe('Bitte wähle ein <u>Thema</u> für dein Training aus')
        self.fields['topic'].required = True
        if settings:
            self.fields['topic'].queryset = Topic.objects.filter(youths=settings.age_group)
        for field in self.fields:
            if field != 'topic':
                self.fields[field].widget = forms.HiddenInput()
            self.fields[field].widget.attrs = {'x-model': field}


class Step2Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'

    def __init__(self, settings=None, initial=None, *args, **kwargs):
        super().__init__(initial=initial, *args, **kwargs)
        self.fields['structure'].label = mark_safe('Bitte wähle eine <u>Struktur</u> für dein Training aus')
        self.fields['structure'].required = True
        if initial and 'topic' in initial and initial['topic'] != '':
            initial['topic'] = initial['topic']
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

    def __init__(self, settings=None, initial=None, *args, **kwargs):
        super().__init__(initial=initial, *args, **kwargs)
        self.fields['block1'].label = mark_safe('Bitte wähle die Übungsart für das <u>Warm-Up</u> aus')
        self.fields['block2'].label = mark_safe('Bitte wähle die Übungsart für den <u>Hauptteil 1</u> aus')
        self.fields['block3'].label = mark_safe('Bitte wähle die Übungsart für den <u>Hauptteil 2</u> aus')
        self.fields['block4'].label = mark_safe('Bitte wähle die Übungsart für den <u>Hauptteil 3</u> aus')
        self.fields['block5'].label = mark_safe('Bitte wähle die Übungsart für den <u>Abschluss</u> aus')
        if initial and 'structure' in initial and initial['structure'] != '':
            structure = Structure.objects.get(pk=initial['structure'])
            for i in range(1, 6):
                self.fields['block{}'.format(i)].required = True
                queryset = getattr(structure, 'blocks{}'.format(i)).all()
                self.fields['block{}'.format(i)].queryset = queryset
                if queryset.count() == 1:
                    self.fields['block{}'.format(i)].empty_label = None
            if not structure.phase5:
                self.fields['block5'].widget = forms.HiddenInput()
                self.fields['block4'].label = mark_safe('Bitte wähle die Übungsart für den <u>Abschluss</u> aus')
        for field in self.fields:
            if field[:5] != 'block':
                self.fields[field].widget = forms.HiddenInput()
            else:
                if self.fields[field].queryset.count() == 1:
                    self.fields[field].widget = forms.HiddenInput()
            self.fields[field].widget.attrs = {'x-model': field}


class Step4Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'

    def __init__(self, settings=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
            self.fields[field].widget = forms.HiddenInput()
            self.fields[field].widget.attrs = {'x-model': field}


class Step5Form(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'

    def __init__(self, settings=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['name', 'description']:
                self.fields[field].widget = forms.HiddenInput()
            self.fields[field].widget.attrs = {'x-model': field}
        self.fields['name'].label = 'Bitte gib einen Namen für die Trainingseinheit an'
        self.fields['description'].label = 'Bitte gib eine Beschreibung für die Trainingseinheit an'


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'

    def __init__(self, settings=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings
        self.fields['user'].required = False
        self.fields['name'].required = False

    def clean_user(self):
        return self.settings

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            return 'Mein Training'
        return name


class TopicForm(forms.Form):
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), label='Nach Thema filtern')

    def __init__(self, settings=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if settings:
            self.fields['topic'].queryset = Topic.objects.filter(youths=settings.age_group)
        for field in self.fields:
            self.fields[field].widget.attrs = {'x-model': field}
