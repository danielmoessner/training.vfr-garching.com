from django.utils.safestring import mark_safe
from apps.generator.models import Topic, Structure, Training
from django import forms


class ShowHideFieldsMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.shown_fields:
            self.show_field(field)
        for field in self.Meta.hidden_fields:
            self.hide_field(field)

    def hide_fields(self, fields):
        fields = list(set(fields))
        remaining_fields = [field for field in self.Meta.fields if field not in fields]
        first_fields = {field: self.fields[field] for field in remaining_fields}
        last_fields = {field: self.fields[field] for field in fields}
        self.fields = {**first_fields, **last_fields}
        for field in fields:
            self.hide_field(field)

    def show_field(self, field):
        self.fields[field].widget.attrs = {'class': 'px-3 py-2', 'x-model': field}

    def hide_field(self, field):
        self.fields[field].label = ''
        self.fields[field].required = False
        self.fields[field].widget.attrs = {'class': 'hidden!', 'x-model': field}


class Step1Form(ShowHideFieldsMixin, forms.ModelForm):
    class Meta:
        model = Training
        shown_fields = []
        hidden_fields = Training.get_remaining_fields(shown_fields)
        fields = shown_fields + hidden_fields

    def __init__(self, settings=None, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Step2Form(ShowHideFieldsMixin, forms.ModelForm):
    class Meta:
        model = Training
        shown_fields = ['structure']
        hidden_fields = Training.get_remaining_fields(shown_fields)
        fields = shown_fields + hidden_fields

    def __init__(self, settings=None, initial=None, *args, **kwargs):
        super().__init__(initial=initial, *args, **kwargs)
        self.fields['structure'].label = mark_safe('Bitte wähle eine <u>Struktur</u> für dein Training aus')
        self.fields['structure'].required = True
        if initial and 'topic' in initial and initial['topic'] != '':
            initial['topic'] = initial['topic']
            topic = Topic.objects.get(pk=initial['topic'])
            self.fields['structure'].queryset = topic.structures.all()


class Step3Form(ShowHideFieldsMixin, forms.ModelForm):
    class Meta:
        model = Training
        shown_fields = []
        hidden_fields = Training.get_remaining_fields(shown_fields)
        fields = shown_fields + hidden_fields

    def __init__(self, settings=None, initial=None, *args, **kwargs):
        super().__init__(initial=initial, *args, **kwargs)
        # self.fields['block1'].label = mark_safe('Bitte wähle die Übungsart für das <u>Warm-Up</u> aus')
        # self.fields['block2'].label = mark_safe('Bitte wähle die Übungsart für den <u>Hauptteil 1</u> aus')
        # self.fields['block3'].label = mark_safe('Bitte wähle die Übungsart für den <u>Hauptteil 2</u> aus')
        # self.fields['block4'].label = mark_safe('Bitte wähle die Übungsart für den <u>Hauptteil 3</u> aus')
        # self.fields['block5'].label = mark_safe('Bitte wähle die Übungsart für den <u>Abschluss</u> aus')
        # fields_to_hide = []
        # if initial and 'structure' in initial and initial['structure'] != '':
        #     structure = Structure.objects.get(pk=initial['structure'])
        #     for i in range(1, 6):
        #         queryset = getattr(structure, 'blocks{}'.format(i)).all()
        #         self.fields['block{}'.format(i)].queryset = queryset
                # if queryset.count() == 1:
                    # fields_to_hide.append('block{}'.format(i))
            # if not structure.phase5:
                # fields_to_hide.append('block5')
                # self.fields['block4'].label = mark_safe('Bitte wähle die Übungsart für den <u>Abschluss</u> aus')
        # for field in self.fields:
        #     if field[:5] == 'block' and self.fields[field].queryset.count() == 1:
        #         fields_to_hide.append(field)
        # self.hide_fields(fields_to_hide)


class Step4Form(ShowHideFieldsMixin, forms.ModelForm):
    class Meta:
        model = Training
        shown_fields = []
        hidden_fields = Training.get_remaining_fields(shown_fields)
        fields = shown_fields + hidden_fields

    def __init__(self, settings=None, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Step5Form(ShowHideFieldsMixin, forms.ModelForm):
    class Meta:
        model = Training
        shown_fields = ['name', 'description']
        hidden_fields = Training.get_remaining_fields(shown_fields)
        fields = shown_fields + hidden_fields

    def __init__(self, settings=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Bitte gib einen Namen für die Trainingseinheit an'
        self.fields['description'].label = 'Bitte gib eine Beschreibung für die Trainingseinheit an'
        self.fields['description'].widget = forms.Textarea({'rows': 10})


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
