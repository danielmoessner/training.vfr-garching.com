from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import ContextMixin
from rest_framework.response import Response

from apps.generator.models import Structure, Topic
from apps.trainings.forms import TrainingForm, Step1Form, Step2Form
from apps.trainings.models import Exercise, Group, Filter, Difficulty
from apps.settings.models import General
from rest_framework.views import APIView
from apps.users.models import UserSettings
from apps.users.forms import SelectAgeGroupForm, SelectDifficultiesForm, SearchForm
from django.views import generic


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
        return context


class FilterContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get or create the settings
        settings, created = UserSettings.objects.get_or_create(user=self.request.user)
        context['user_settings'] = settings
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
    success_url = reverse_lazy('training_list')

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


class TrainingListView(LoginRequiredMixin, SettingsContextMixin, FilterContextMixin, generic.TemplateView):
    template_name = 'trainings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # trainings
        trainings = Exercise.objects.all()
        if context['user_settings'].search:
            trainings = Exercise.get_search_queryset(context['user_settings'].search, trainings)
        trainings_list = Exercise.get_trainings_list(context['user_settings'], trainings)
        context['trainings'] = trainings_list
        # count
        for training_filter in list(self.request.user.settings.training_filters.all()):
            trainings = trainings.filter(filters=training_filter.pk)
        context['trainings_count'] = trainings.count()
        # return
        return context


class SearchView(TrainingListView):
    template_name = 'trainings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # search
        search = self.request.GET.get('suche')
        if search:
            trainings = Exercise.objects.filter(
                Q(name__icontains=search) | Q(filters__name__icontains=search)
            ).distinct()
            trainings = Exercise.get_trainings_list(context['user_settings'], trainings)
            context['trainings'] = trainings
            context['search'] = search
        context['trainings_count'] = '"?"'
        # return
        return context


class BookmarksView(TrainingListView):
    template_name = 'trainings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookmarked_trainings = self.request.user.settings.bookmarks.all()
        if context['user_settings'].search:
            bookmarked_trainings = Exercise.get_search_queryset(context['user_settings'].search, bookmarked_trainings)
        trainings = Exercise.get_trainings_list(context['user_settings'], bookmarked_trainings)
        context['trainings'] = trainings
        context['trainings_count'] = '"?"'
        return context


class TrainingDetailView(LoginRequiredMixin, SettingsContextMixin, FilterContextMixin, generic.DetailView):
    template_name = 'training.html'
    model = Exercise

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmarked'] = self.request.user.settings.bookmarks.filter(pk=self.object.pk).exists()
        context['trainings_count'] = '"1"'
        return context


class GeneratorView(LoginRequiredMixin, SettingsContextMixin, generic.CreateView):
    template_name = 'generator.html'

    def get_form_class(self):
        step = self.request.GET.get('step', default='1')
        # if step == "1":
        #     return Step1Form
        # elif step == "2":
        #     return Step2Form
        return TrainingForm

    def form_valid(self, form):
        step = self.request.GET.get('step', '1')
        if step == '1' or step == '2' or step == '3':
            context = self.get_context_data(form=form)
            context['formdata'] = form.cleaned_data
            return self.render_to_response(context)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['structures'] = Structure.objects.all()
        context['topics'] = Topic.objects.select_related('block1', 'block2', 'block3', 'block4', 'block5').all()
        context['step1form'] = Step1Form()
        step = self.request.GET.get('step', default='1')
        if step == '1':
            context['step'] = 1
        elif step == '2':
            if 'form' in kwargs:
                form = kwargs['form']
                structure = form.cleaned_data['structure']
                topic = form.cleaned_data['topic']
                context['possible_exercises'] = {
                    1: Exercise.filter_by_topic_and_block(topic, structure.block1, structure.phase1),
                    2: Exercise.filter_by_topic_and_block(topic, structure.block2, structure.phase2),
                    3: Exercise.filter_by_topic_and_block(topic, structure.block3, structure.phase3),
                    4: Exercise.filter_by_topic_and_block(topic, structure.block4, structure.phase4),
                    5: Exercise.filter_by_topic_and_block(topic, structure.block5, structure.phase5),
                }
            else:
                context['possible_exercises'] = {
                    1: Exercise.objects.all(),
                    2: Exercise.objects.all(),
                    3: Exercise.objects.all(),
                    4: Exercise.objects.all(),
                    5: Exercise.objects.all(),
                }
            context['step'] = 2
        elif step == '3':
            if 'form' in kwargs:
                data = kwargs['form'].cleaned_data
                context['topic'] = data['topic']
                context['name'] = data['name']
                context['structure'] = data['structure']
                context['exercise1'] = data['exercise1']
                context['exercise2'] = data['exercise2']
                context['exercise3'] = data['exercise3']
                context['exercise4'] = data['exercise4']
                context['exercise5'] = data['exercise5']
            context['step'] = 3
        return context


# save settings views
class AgeGroupFormView(LoginRequiredMixin, SuccessUrlReverseMixin, UpdateUserSettingsMixin, generic.UpdateView):
    form_class = SelectAgeGroupForm


class DifficultiesFormView(LoginRequiredMixin, SuccessUrlReverseMixin, UpdateUserSettingsMixin, generic.UpdateView):
    form_class = SelectDifficultiesForm


class SearchFormView(LoginRequiredMixin, SuccessUrlReverseMixin, UpdateUserSettingsMixin, generic.UpdateView):
    form_class = SearchForm


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
        return HttpResponseRedirect(reverse('training_detail', args=[self.object.pk]))


class ResetSearchView(LoginRequiredMixin, SuccessUrlReverseMixin, generic.View):
    success_url = reverse_lazy('training_list')

    def get(self, request, *args, **kwargs):
        self.request.user.settings.search = ''
        self.request.user.settings.save()
        return HttpResponseRedirect(self.get_success_url())


class ResetAgeGroupView(LoginRequiredMixin, SuccessUrlReverseMixin, generic.View):
    success_url = reverse_lazy('training_list')

    def get(self, request, *args, **kwargs):
        self.request.user.settings.age_group = None
        self.request.user.settings.save()
        return HttpResponseRedirect(self.get_success_url())


class ResetTrainingFiltersView(LoginRequiredMixin, SuccessUrlReverseMixin, generic.View):
    success_url = reverse_lazy('training_list')

    def get(self, request, *args, **kwargs):
        self.request.user.settings.training_filters.set([])
        self.request.user.settings.filter_groups.set(Group.objects.filter(group=None))
        self.request.user.settings.save()
        return HttpResponseRedirect(self.get_success_url())


class ResetDifficultyView(LoginRequiredMixin, SuccessUrlReverseMixin, generic.View):
    success_url = reverse_lazy('training_list')

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
