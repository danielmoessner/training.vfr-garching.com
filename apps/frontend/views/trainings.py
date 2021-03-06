from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin
from django.template.loader import render_to_string
from apps.trainings.models import Exercise, Filter, PlayerAmount
from apps.generator.models import Structure, Topic, Block, Training, Group, TrainingGroup
from apps.generator.forms import Step1Form, Step2Form, Step3Form, Step5Form, TrainingForm, Step4Form, TopicForm
from apps.settings.models import Trainings
from apps.frontend.utils import get_params_from_request
from django.views import generic
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse, reverse_lazy
from weasyprint import HTML
from .utils import SettingsContextMixin
import random


# mixins
class TrainingContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        # super
        context = super().get_context_data(**kwargs)
        # add all selected values to the context
        training_pk = self.request.GET.get('training', default=None)
        if training_pk and training_pk != '0':
            context['training'] = Training.objects.get(pk=training_pk)
        topic_pk = self.request.GET.get('topic', default=None)
        if topic_pk and topic_pk != '0':
            context['topic'] = Topic.objects.get(pk=topic_pk)
        structure_pk = self.request.GET.get('structure', default=None)
        if structure_pk and structure_pk != '0':
            context['structure'] = Structure.objects.get(pk=structure_pk)
        for i in range(1, 6):
            block_pk = self.request.GET.get('block{}'.format(i), default=None)
            if block_pk and block_pk != '0':
                context['block{}'.format(i)] = Block.objects.get(pk=block_pk)
        for i in range(1, 6):
            exercise_pk = self.request.GET.get('exercise{}'.format(i), default=None)
            if exercise_pk and exercise_pk != '0':
                context['exercise{}'.format(i)] = Exercise.objects.select_related('difficulty').get(pk=exercise_pk)
        name = self.request.GET.get('name', default=None)
        if name:
            context['name'] = name
        description = self.request.GET.get('description', default=None)
        if description:
            context['description'] = description  # .replace('\n', '')
        player_amount = self.request.GET.get('player_amount', default=None)
        if player_amount:
            context['player_amount'] = player_amount
        exercise_amount = self.request.GET.get('exercise_amount', default=None)
        if exercise_amount:
            context['exercise_amount'] = exercise_amount
        # return
        return context


# views
class TrainingsView(LoginRequiredMixin, SettingsContextMixin, generic.ListView):
    template_name = 'trainings.html'
    model = Training

    def get_queryset(self):
        return Training.optimize_queryset(self.request.user.settings.trainings.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercises'] = Exercise.optimize_queryset()
        context['form'] = TopicForm(settings=self.request.user.settings)
        context['groups'] = Group.optimize_queryset(user_settings=context['user_settings'])
        context['title'] = 'Meine Trainings'
        return context


class TrainingsVfrView(LoginRequiredMixin, SettingsContextMixin, generic.ListView):
    template_name = 'trainings_vfr.html'
    model = Training

    def get_queryset(self):
        return Training.optimize_queryset(Training.objects.filter(user=None))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['exercises'] = Exercise.optimize_queryset()
        context['training_groups'] = TrainingGroup.objects.prefetch_related('trainings',
                                                                            'trainings__topic',
                                                                            'trainings__exercise1',
                                                                            'trainings__exercise2',
                                                                            'trainings__exercise3',
                                                                            'trainings__exercise4',
                                                                            'trainings__exercise5')
        context['groups'] = Group.optimize_queryset(user_settings=context['user_settings'])
        context['title'] = 'VfR Trainings'
        return context


class TrainingView(LoginRequiredMixin, TrainingContextMixin, SettingsContextMixin, generic.TemplateView):
    template_name = 'training.html'

    def get_context_data(self, **kwargs):
        # super
        context = super().get_context_data(**kwargs)
        # exercises for the pop up
        context['exercises'] = []
        for i in range(1, 6):
            if 'exercise{}'.format(i) in context:
                context['exercises'].append(context['exercise{}'.format(i)])
        # print url
        context['print_url'] = '{}?{}'.format(reverse('training_print'), get_params_from_request(self.request))
        # return
        return context


class TrainingPrintView(LoginRequiredMixin, TrainingContextMixin, SettingsContextMixin, generic.TemplateView):
    template_name = 'training_pdf.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = {**context}
        return context

    def render_to_response(self, context, **response_kwargs):
        import logging
        import os

        logger = logging.getLogger('weasyprint')
        logger.handlers = []  # Remove the default stderr handler
        logger.addHandler(logging.FileHandler(os.path.join(settings.BASE_DIR, '/tmp/weasyprint.log')))

        rendered = render_to_string(self.template_name, context)
        name = context['name']
        html = HTML(string=rendered, base_url=self.request.build_absolute_uri())
        pdf = html.write_pdf()
        response = HttpResponse(pdf)
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(name)
        return response


class DeleteTrainingView(LoginRequiredMixin, SettingsContextMixin, generic.DeleteView):
    model = Training
    success_url = reverse_lazy('trainings')


class GeneratorView(LoginRequiredMixin, TrainingContextMixin, SettingsContextMixin, generic.FormView):
    template_name = 'generator.html'
    success_url = reverse_lazy('trainings')

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        # set initial data from get parameters
        initial_data_from_get_parameters = dict()
        for key, value in self.request.GET.items():
            initial_data_from_get_parameters[key] = self.request.GET.get(key)
        kwargs = self.get_form_kwargs()
        initial_data = {**initial_data_from_get_parameters, **kwargs['initial']}
        kwargs.pop('initial')
        if self.request.method == 'POST':
            return form_class(settings=self.request.user.settings, initial=initial_data, **kwargs)
        return form_class(initial=initial_data, settings=self.request.user.settings, **kwargs)

    def get_form_class(self):
        step = self.request.GET.get('step', '1')
        if self.request.method == 'GET':
            if step == '1':
                return Step1Form
            elif step == '2':
                return Step2Form
            elif step == '3':
                return Step3Form
            elif step == '4':
                return Step4Form
            elif step == '5':
                return Step5Form
        return TrainingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs

    def post(self, request, *args, **kwargs):
        training_pk = self.request.GET.get('training', default=None)
        if training_pk and Training.objects.filter(user=self.request.user.settings, pk=training_pk).exists():
            self.object = Training.objects.get(pk=training_pk)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # general stuff
        context['page'] = Trainings.get_solo()
        # print url
        context['link_url'] = '{}{}?{}&name=Training'.format(settings.URL, reverse('training'),
                                                             get_params_from_request(self.request))
        # try to edit
        training_pk = self.request.GET.get('training', default=None)
        if training_pk and Training.objects.filter(user=self.request.user.settings, pk=training_pk).exists():
            context['training'] = Training.objects.get(pk=training_pk)
        # steps
        step = self.request.GET.get('step', default='1')
        context['step'] = step
        exercise_step = self.request.GET.get('exercise_step', default='0')
        context['exercise_step'] = exercise_step
        # step specific context of what the user can select
        if step == '1':
            context['groups'] = Group.optimize_queryset(user_settings=context['user_settings'])
            context['topics'] = Topic.objects.all()
        elif step == '2':
            if 'topic' in context:
                context['structures'] = context['topic'].structures.all()
            else:
                context['structures'] = Structure.objects.all()
        elif step == '3':
            if 'structure' in context:
                for i in range(1, 6):
                    blocks = getattr(context['structure'], 'blocks{}'.format(i))
                    if blocks.count() == 1:
                        context['block{}'.format(i)] = blocks.first()
            else:
                context['blocks'] = Block.objects.all()
        elif step == '4':
            context['exercises_total'] = Exercise.objects.all().count()
            context['possible_exercises'] = Exercise.objects.all().select_related('difficulty')
            # new stuff
            if 'topic' in context:
                context['possible_exercises'] = Exercise.filter_by_topic_new(
                    context['possible_exercises'],
                    context['topic']
                )
            if 'player_amount' in context:
                player_amount_id = int(context['player_amount'])
                context['possible_exercises'] = context['possible_exercises'].filter(
                    player_amounts=PlayerAmount.objects.get(id=player_amount_id))
            context['training_filters'] = Filter.objects.filter(show_on_trainings_generator_step_4=True)
            context['training_filters_2'] = Filter.objects.filter(show_on_trainings_generator_step_4_row_2=True)

            if context['user_settings'].search:
                context['possible_exercises'] = (
                    Exercise
                        .get_search_queryset(context['user_settings'].search, context['possible_exercises'])
                        .select_related('difficulty')
                )
        if step in ['4', '5']:
            exercise_pks = []
            for i in range(1, 6):
                exercise_pks.append(self.request.GET.get('exercise{}'.format(i), default='0'))
            exercise_pks = list(filter(lambda x: x != '', exercise_pks))
            exercises1 = Exercise.objects.filter(pk__in=exercise_pks).select_related('difficulty').prefetch_related(
                'filters')
            context['exercises'] = list(exercises1)
            if step == '4':
                exercises2 = context['possible_exercises'].exclude(pk__in=exercise_pks).select_related(
                    'difficulty').prefetch_related('filters')
                context['exercises'] = context['exercises'] + list(exercises2)

        # random
        if 'possible_exercises' in context:
            context['possible_exercises'] = list(context['possible_exercises'])
            random.shuffle(context['possible_exercises'])
        # return
        return context
