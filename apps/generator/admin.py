from apps.generator.models import Block, Topic, Structure, StructureBlock
from apps.trainings.models import Filter
from apps.trainings.admin import FilterWidget
from django.contrib import admin
from django import forms


# overwrite block admin
class BlockForm(forms.ModelForm):
    or_filters = forms.ModelMultipleChoiceField(
        queryset=Filter.objects.all(),
        widget=FilterWidget(name='or'),
        label="ODER Filter",
        required=False
    )
    and_filters = forms.ModelMultipleChoiceField(
        queryset=Filter.objects.all(),
        widget=FilterWidget(name='and'),
        label="UND Filter",
        required=False
    )

    class Meta:
        model = Block
        fields = '__all__'


class BlockAdmin(admin.ModelAdmin):
    form = BlockForm


admin.site.register(Block, BlockAdmin)


# overwrite topic admin
class TopicForm(forms.ModelForm):
    or_filters = forms.ModelMultipleChoiceField(
        queryset=Filter.objects.all(),
        widget=FilterWidget(name='or'),
        label="ODER Filter",
        required=False
    )

    class Meta:
        model = Topic
        fields = '__all__'


class TopicAdmin(admin.ModelAdmin):
    form = TopicForm


admin.site.register(Topic, TopicAdmin)

# normal admins
admin.site.register(Structure)
admin.site.register(StructureBlock)
