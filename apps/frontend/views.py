from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.template.loader import render_to_string
from django.views.generic.base import ContextMixin
from rest_framework.response import Response
from apps.settings.models import Trainings
from apps.trainings.models import Exercise, Group, Filter, Difficulty
from apps.generator.models import Structure, Topic, Block, Training
from apps.generator.forms import Step1Form, Step2Form, Step3Form, Step5Form, TrainingForm, Step4Form, TopicForm
from apps.settings.models import General
from rest_framework.views import APIView
from apps.users.models import UserSettings
from apps.users.forms import SelectAgeGroupForm, SelectDifficultiesForm, SearchForm, UserSettingsForm
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from weasyprint import HTML


# mixins
class SuccessUrlReverseMixin:
    def get_success_url(self):
        if self.request.GET.get('reverse'):
            self.success_url = self.request.GET.get('reverse')
        return self.success_url


class SettingsContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = General.get_solo()
        # get or create the settings
        if self.request.user.is_authenticated:
            settings, created = UserSettings.objects.get_or_create(user=self.request.user)
            context['user_settings'] = settings
        return context


class FilterContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user settings
        settings, created = UserSettings.objects.get_or_create(user=self.request.user)
        # forms
        context['age_group_form'] = SelectAgeGroupForm(instance=settings)
        context['difficulties_form'] = SelectDifficultiesForm(instance=settings)
        # settings
        context['groups_open'] = self.request.user.settings.get_filter_groups()
        context['filters_selected'] = self.request.user.settings.get_training_filters()
        # calculate count
        context['trainings_total'] = Exercise.objects.all().count()
        # filters and groups
        context['root_group_pks'] = [group.pk for group in Group.objects.filter(group=None)]
        context['groups'] = Group.get_groups_dict(settings=settings)
        context['training_filters'] = Filter.objects.all()
        # return
        return context


class UpdateUserSettingsMixin:
    model = UserSettings
    success_url = reverse_lazy('exercises')

    def post(self, request, *args, **kwargs):
        settings, created = UserSettings.objects.get_or_create(user=self.request.user)
        self.object = settings
        form = self.get_form()
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(self.get_success_url())


# views
class LoginView(SettingsContextMixin, DjangoLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    redirect_field_name = 'next'


class LogoutView(DjangoLogoutView):
    pass


class ExerciseListView(LoginRequiredMixin, SettingsContextMixin, FilterContextMixin, generic.TemplateView):
    template_name = 'exercises.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # trainings
        trainings = Exercise.objects.all()
        if context['user_settings'].search:
            trainings = Exercise.get_search_queryset(context['user_settings'].search, trainings)
        trainings_list = Exercise.get_trainings_list(context['user_settings'], trainings)
        context['exercises'] = trainings_list
        context['all_exercises'] = Exercise.objects.select_related('difficulty').prefetch_related('filters').all()
        # count
        for training_filter in list(self.request.user.settings.training_filters.all()):
            trainings = trainings.filter(filters=training_filter.pk)
        context['trainings_count'] = trainings.count()
        # return
        return context


class BookmarksView(ExerciseListView):
    template_name = 'exercises.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookmarked_trainings = self.request.user.settings.bookmarks.all()
        if context['user_settings'].search:
            bookmarked_trainings = Exercise.get_search_queryset(context['user_settings'].search, bookmarked_trainings)
        exercises = Exercise.get_trainings_list(context['user_settings'], bookmarked_trainings)
        context['exercises'] = exercises
        context['all_exercises'] = bookmarked_trainings.select_related('difficulty').prefetch_related('filters')
        context['trainings_count'] = '"?"'
        return context


class ExerciseDetailView(LoginRequiredMixin, SettingsContextMixin, FilterContextMixin, generic.DetailView):
    template_name = 'exercise.html'
    model = Exercise

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmarked'] = self.request.user.settings.bookmarks.filter(pk=self.object.pk).exists()
        context['trainings_count'] = '"1"'
        return context


class ExercisePdfView(LoginRequiredMixin, SettingsContextMixin, generic.DetailView):
    model = Exercise
    template_name = 'exercise_pdf.html'

    def render_to_response(self, context, **response_kwargs):
        rendered = render_to_string(self.template_name, context)
        html = HTML(string=rendered, base_url=self.request.build_absolute_uri())
        pdf = html.write_pdf()
        # return HttpResponseRedirect('/media/pdfs/{}.pdf'.format(self.object.pk))
        response = HttpResponse(pdf)
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(self.object.name)
        return response


class TrainingsView(LoginRequiredMixin, SettingsContextMixin, generic.ListView):
    template_name = 'trainings.html'
    model = Training

    def get_queryset(self):
        return self.request.user.settings.trainings.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercises'] = Exercise.objects.select_related('difficulty').prefetch_related('filters')
        context['form'] = TopicForm(settings=self.request.user.settings)
        return context


class TrainingsVfrView(LoginRequiredMixin, SettingsContextMixin, generic.ListView):
    template_name = 'trainings.html'
    model = Training

    def get_queryset(self):
        return Training.objects.filter(user=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercises'] = Exercise.objects.select_related('difficulty').prefetch_related('filters')
        context['form'] = TopicForm(settings=self.request.user.settings)
        return context


class TrainingView(LoginRequiredMixin, SettingsContextMixin, generic.DetailView):
    model = Training
    template_name = 'training.html'


class TrainingPdfView(LoginRequiredMixin, SettingsContextMixin, generic.DetailView):
    model = Training
    template_name = 'training.html'

    def render_to_response(self, context, **response_kwargs):
        rendered = render_to_string(self.template_name, context)
        html = HTML(string=rendered, base_url=self.request.build_absolute_uri())
        pdf = html.write_pdf()
        # return HttpResponseRedirect('/media/pdfs/{}.pdf'.format(self.object.pk))
        response = HttpResponse(pdf)
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(self.object.name)
        return response


class DeleteTrainingView(LoginRequiredMixin, SettingsContextMixin, generic.DeleteView):
    model = Training
    success_url = reverse_lazy('trainings')


class UpdateTrainingView(LoginRequiredMixin, SettingsContextMixin, generic.UpdateView):
    model = Training
    success_url = ''


class GeneratorView(LoginRequiredMixin, SettingsContextMixin, generic.FormView):
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
        # try to edit
        training_pk = self.request.GET.get('training', default=None)
        if training_pk and Training.objects.filter(user=self.request.user.settings, pk=training_pk).exists():
            context['training'] = Training.objects.get(pk=training_pk)
        # steps
        step = self.request.GET.get('step', default='1')
        context['step'] = step
        exercise_step = self.request.GET.get('exercise_step', default='0')
        context['exercise_step'] = exercise_step
        # add all selected values to the context
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
        # step specific context of what the user can select
        if step == '1':
            context['topics'] = Topic.objects.all()
        elif step == '2':
            context['structures'] = Structure.objects.all()
        elif step == '3':
            context['blocks'] = Block.objects.all()
            for i in range(1, 6):
                if context['form'].fields['block{}'.format(i)].queryset.count() == 1:
                    context['block{}'.format(i)] = context['form'].fields['block{}'.format(i)].queryset.first()
        elif step == '4':
            context['exercises_total'] = Exercise.objects.all().count()
            context['possible_exercises'] = Exercise.objects.all().select_related('difficulty')
            if 'block{}'.format(exercise_step) in context:
                context['possible_exercises'] = Exercise.filter_by_block(context['possible_exercises'],
                                                                         context['block{}'.format(exercise_step)])
            if 'structure' in context and 'topic' in context:
                phase = getattr(context['structure'], 'phase{}'.format(exercise_step))
                context['possible_exercises'] = Exercise.filter_by_topic(
                    context['possible_exercises'],
                    context['topic'],
                    phase
                )
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
        # return
        return context


class GeneratorPrintView(LoginRequiredMixin, SettingsContextMixin, generic.FormView):
    form_class = TrainingForm
    template_name = 'training.html'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        training = form.save()
        context = {
            'object': training
        }
        rendered = render_to_string(self.template_name, context)
        name = training.name
        training.delete()
        html = HTML(string=rendered, base_url=self.request.build_absolute_uri())
        pdf = html.write_pdf()
        # return HttpResponseRedirect('/media/pdfs/{}.pdf'.format(self.object.pk))
        response = HttpResponse(pdf)
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(name)
        return response


# save settings views
class SettingsView(LoginRequiredMixin, SettingsContextMixin, generic.UpdateView):
    template_name = 'settings.html'
    form_class = SelectAgeGroupForm
    success_url = reverse_lazy('settings')

    def get_object(self, queryset=None):
        return self.request.user.settings


class AgeGroupFormView(LoginRequiredMixin, SuccessUrlReverseMixin, UpdateUserSettingsMixin, generic.UpdateView):
    form_class = SelectAgeGroupForm


class DifficultiesFormView(LoginRequiredMixin, SuccessUrlReverseMixin, UpdateUserSettingsMixin, generic.UpdateView):
    form_class = SelectDifficultiesForm


class SearchFormView(LoginRequiredMixin, UpdateUserSettingsMixin, generic.UpdateView):
    form_class = SearchForm

    def get_success_url(self):
        return self.request.POST.get('reverse')


# get change views
class BookmarkTrainingView(LoginRequiredMixin, generic.DetailView):
    model = Exercise

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        bookmarks = list(self.request.user.settings.bookmarks.all())
        if self.object in bookmarks:
            self.request.user.settings.bookmarks.remove(self.object.pk)
        else:
            self.request.user.settings.bookmarks.add(self.object.pk)
        self.request.user.settings.save()
        return HttpResponseRedirect(reverse('favorites'))


class ResetAgeGroupView(LoginRequiredMixin, SuccessUrlReverseMixin, generic.View):
    success_url = reverse_lazy('exercises')

    def get(self, request, *args, **kwargs):
        self.request.user.settings.age_group = None
        self.request.user.settings.save()
        return HttpResponseRedirect(self.get_success_url())


class ResetTrainingFiltersView(LoginRequiredMixin, SuccessUrlReverseMixin, generic.View):
    success_url = reverse_lazy('exercises')

    def get(self, request, *args, **kwargs):
        self.request.user.settings.training_filters.set([])
        self.request.user.settings.filter_groups.set(Group.objects.filter(group=None))
        self.request.user.settings.save()
        return HttpResponseRedirect(self.get_success_url())


class ResetDifficultyView(LoginRequiredMixin, SuccessUrlReverseMixin, generic.View):
    success_url = reverse_lazy('exercises')

    def get(self, request, *args, **kwargs):
        self.request.user.settings.difficulties.set(Difficulty.objects.all())
        self.request.user.settings.save()
        return HttpResponseRedirect(self.get_success_url())


# api views
class ToggleFilterGroupApiView(APIView):
    def post(self, request, pk=None):
        if self.request.user.settings.filter_groups.filter(pk=pk).exists():
            self.request.user.settings.filter_groups.remove(pk)
            action = 'removed'
        else:
            self.request.user.settings.filter_groups.add(pk)
            action = 'added'
        data = {
            'status': 'ok',
            'action': action
        }
        return Response(data)


class ToggleTrainingFilterApiView(APIView):
    def post(self, request, pk=None):
        user_settings = request.user.settings
        user_training_filters = user_settings.training_filters
        if user_training_filters.filter(pk=pk).exists():
            user_training_filters.remove(pk)
            action = 'removed'
        else:
            user_training_filters.add(pk)
            action = 'added'
        trainings = Exercise.objects.all()
        if user_settings.search:
            trainings = Exercise.get_search_queryset(user_settings.search, trainings)
        for training_filter in list(user_training_filters.all()):
            trainings = trainings.filter(filters=training_filter.pk)
        data = {
            'status': 'ok',
            'action': action,
            'videos': trainings.count()
        }
        return Response(data)


class SearchApiView(APIView):
    def get(self, request):
        search = request.GET.get('search', default='')
        if search:
            exercises = Exercise.search(Exercise.objects.all(), search)[:5]
            exercises = [{'name': result.name, 'type': 'EXERCISE', 'focus': result.focus} for result in exercises]
            filters = Filter.search(Filter.objects.all(), search)[:5]
            filters = [{'name': result.name, 'type': 'FILTER'} for result in filters]
            results = {'exercises': exercises, 'filters': filters}
            data = results
        else:
            data = {'exercises': [], 'filters': []}
        return Response(data)
