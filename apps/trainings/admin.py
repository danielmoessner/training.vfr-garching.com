from apps.trainings.models import Filter, Exercise, Group, Youth, Difficulty, PlayerAmount
from django.contrib import admin
from django import forms
from datetime import date


# keep this widget for example purposes
class DateSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        days = [(day, day) for day in range(1, 32)]
        months = [(month, month) for month in range(1, 13)]
        years = [(year, year) for year in [2018, 2019, 2020]]
        widgets = [
            forms.Select(attrs=attrs, choices=days),
            forms.Select(attrs=attrs, choices=months),
            forms.Select(attrs=attrs, choices=years),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.day, value.month, value.year]
        elif isinstance(value, str):
            year, month, day = value.split('-')
            return [day, month, year]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        day, month, year = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.
        return '{}-{}-{}'.format(year, month, day)


# overwrite training admin
class FilterWidget(forms.Widget):
    template_name = 'trainings/training_filter_widget.html'

    def __init__(self, name=None, attrs=None):
        super().__init__(attrs)
        self.name = name if name else ''

    def get_inputs(self, values):
        inputs = {}
        for training_filter in Filter.objects.all():
            checkbox = forms.CheckboxInput()
            attrs = {
                'label': training_filter.name,
                'style': 'width: 16px; height: 16px; margin: 0;'
            }
            checked = False
            if values and training_filter.pk in values:
                checked = True
            name = '{}{}'.format(self.name, training_filter.pk)
            inputs[training_filter.pk] = checkbox.get_context(name, checked, attrs)['widget']
        return inputs

    def get_context(self, name, values, attrs):
        context = super().get_context(name, values, attrs)
        context['widgets'] = self.get_inputs(values)
        context['groups'] = Group.get_groups_dict(show_hidden=True)
        context['root_group_pks'] = [group.pk for group in Group.objects.filter(group=None)]
        return context

    def value_from_datadict(self, data, files, name):
        values = []
        for training_filter in Filter.objects.all():
            name = '{}{}'.format(self.name, training_filter.pk)
            if name in data:
                values.append(training_filter.pk)
        return values


class TrainingForm(forms.ModelForm):
    filters = forms.ModelMultipleChoiceField(
        queryset=Filter.objects.all(),
        widget=FilterWidget(),
        label="Filter", required=False)
    player_amounts = forms.ModelMultipleChoiceField(queryset=PlayerAmount.objects.all(), label='Spieleranzahlen',
                                                    widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Exercise
        fields = '__all__'


class TrainingAdmin(admin.ModelAdmin):
    form = TrainingForm
    list_display = ('name', 'focus')
    search_fields = ('name', 'focus')


admin.site.register(Exercise, TrainingAdmin)


# overwrite training filter admin
class TrainingFilterForm(forms.ModelForm):
    trainings = forms.ModelMultipleChoiceField(queryset=Exercise.objects.all(), required=False)

    class Meta:
        model = Filter
        exclude = ['show_on_detail']


class TrainingFilterAdmin(admin.ModelAdmin):
    form = TrainingFilterForm
    list_display = ('name', 'ordering', 'hide', 'show_on_detail_bottom', 'exercises_count')

    def exercises_count(self, obj):
        return obj.trainings.all().count()

    exercises_count.short_description = "Übungen Anzahl"

    def get_queryset(self, request):
        return Filter.objects.all().prefetch_related('trainings')

    def save_model(self, request, obj, form, change):
        # save without m2m field (can't save them until obj has id)
        super(TrainingFilterAdmin, self).save_model(request, obj, form, change)
        # if that worked, deal with m2m field
        obj.trainings.clear()
        for training in form.cleaned_data['trainings']:
            training.filters.add(obj)

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form.base_fields['trainings'].initial = [o.pk for o in obj.trainings.all()]
        else:
            self.form.base_fields['trainings'].initial = []
        return super(TrainingFilterAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Filter, TrainingFilterAdmin)


# default admin for filter and group
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')


admin.site.register(Group, GroupAdmin)
admin.site.register(Youth)
admin.site.register(Difficulty)
admin.site.register(PlayerAmount)
# admin.site.register(Training)
