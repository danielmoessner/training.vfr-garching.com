from apps.generator.models import Block, Topic, Structure, Training, Group
from apps.trainings.models import Filter
from apps.trainings.admin import FilterWidget
from django.contrib import admin
from django import forms


# overwrite block admin
# class BlockForm(forms.ModelForm):
#     or_filters = forms.ModelMultipleChoiceField(
#         queryset=Filter.objects.all(),
#         widget=FilterWidget(name='or'),
#         label="ODER Filter",
#         required=False
#     )
#     and_filters = forms.ModelMultipleChoiceField(
#         queryset=Filter.objects.all(),
#         widget=FilterWidget(name='and'),
#         label="UND Filter",
#         required=False
#     )
#
#     class Meta:
#         model = Block
#         fields = '__all__'


# class BlockAdmin(admin.ModelAdmin):
#     form = BlockForm


# admin.site.register(Block, BlockAdmin)


# overwrite topic admin
class TopicForm(forms.ModelForm):
    general_or_filters = forms.ModelMultipleChoiceField(
        queryset=Filter.objects.all(),
        widget=FilterWidget(name='general_or'),
        label="ALLGEMEINE ODER Filter",
        required=False
    )
    # start_or_filters = forms.ModelMultipleChoiceField(
    #     queryset=Filter.objects.all(),
    #     widget=FilterWidget(name='start_or'),
    #     label="WARM-UP ODER Filter",
    #     required=False
    # )
    # main_or_filters = forms.ModelMultipleChoiceField(
    #     queryset=Filter.objects.all(),
    #     widget=FilterWidget(name='main_or'),
    #     label="HAUPTTEIL ODER Filter",
    #     required=False
    # )
    # end_or_filters = forms.ModelMultipleChoiceField(
    #     queryset=Filter.objects.all(),
    #     widget=FilterWidget(name='end_or'),
    #     label="ABSCHLUSS ODER Filter",
    #     required=False
    # )

    class Meta:
        model = Topic
        fields = '__all__'


class TopicAdmin(admin.ModelAdmin):
    form = TopicForm


admin.site.register(Topic, TopicAdmin)

# normal admins
# admin.site.register(Structure)
admin.site.register(Group)


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


admin.site.register(Training, TrainingAdmin)
