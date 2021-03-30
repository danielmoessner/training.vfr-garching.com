from apps.trainings.models import TrainingFilter, Training, FilterGroup, AgeGroup
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
class TrainingFilterWidget(forms.Widget):
    template_name = 'trainings/training_filter_widget.html'

    def get_inputs(self, values):
        inputs = {}
        for training_filter in TrainingFilter.objects.all():
            checkbox = forms.CheckboxInput()
            attrs = {
                'label': training_filter.name,
                'style': 'width: 16px; height: 16px; margin: 0;'
            }
            checked = False
            if values and training_filter.pk in values:
                checked = True
            inputs[training_filter.pk] = checkbox.get_context(training_filter.pk, checked, attrs)['widget']
        return inputs

    def get_context(self, name, values, attrs):
        context = super().get_context(name, values, attrs)
        context['widgets'] = self.get_inputs(values)
        context['groups'] = FilterGroup.get_groups_dict(show_hidden=True)
        context['root_group_pks'] = [group.pk for group in FilterGroup.objects.filter(group=None)]
        return context

    def value_from_datadict(self, data, files, name):
        values = []
        for training_filter in TrainingFilter.objects.all():
            if str(training_filter.pk) in data:
                values.append(training_filter.pk)
        return values


class TrainingForm(forms.ModelForm):
    filters = forms.ModelMultipleChoiceField(
        queryset=TrainingFilter.objects.all(),
        widget=TrainingFilterWidget(),
        label="Filteroptionen", required=False)

    class Meta:
        model = Training
        fields = '__all__'


class TrainingAdmin(admin.ModelAdmin):
    form = TrainingForm


admin.site.register(Training, TrainingAdmin)


# overwrite training filter admin
class TrainingFilterForm(forms.ModelForm):
    trainings = forms.ModelMultipleChoiceField(queryset=Training.objects.all(), required=False)

    class Meta:
        model = TrainingFilter
        fields = '__all__'


class TrainingFilterAdmin(admin.ModelAdmin):
    form = TrainingFilterForm

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


admin.site.register(TrainingFilter, TrainingFilterAdmin)

# default admin for filter and group
admin.site.register(FilterGroup)
admin.site.register(AgeGroup)
