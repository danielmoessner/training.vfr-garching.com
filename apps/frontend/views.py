from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import ContextMixin
from rest_framework.response import Response
from apps.trainings.models import Training, FilterGroup, TrainingFilter, AgeGroup
from apps.settings.models import General
from rest_framework.views import APIView
from apps.users.models import UserSettings
from apps.users.forms import SelectAgeGroupForm, SelectDifficultiesForm
from django.views import generic


# mixins
class SettingsContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = General.get_solo()
        return context


class FilterContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings, created = UserSettings.objects.get_or_create(user=self.request.user)
        trainings = Training.objects.filter(difficulty__in=settings.difficulties.all())
        context['groups'] = FilterGroup.get_groups_dict(settings=settings)
        context['root_group_pks'] = [group.pk for group in FilterGroup.objects.filter(group=None)]
        context['age_group_form'] = SelectAgeGroupForm(instance=settings)
        context['difficulties_form'] = SelectDifficultiesForm(instance=settings)
        context['trainings'] = trainings
        context['groups_open'] = self.request.user.settings.get_filter_groups()
        context['filters_selected'] = self.request.user.settings.get_training_filters()
        for training_filter in list(settings.training_filters.all()):
            trainings = trainings.filter(filters=training_filter.pk)
        context['videos_count'] = trainings.count()
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
        return HttpResponseRedirect(self.success_url)


# views
class LoginView(SettingsContextMixin, DjangoLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    redirect_field_name = 'next'


class LogoutView(DjangoLogoutView):
    pass


class TrainingListView(LoginRequiredMixin, SettingsContextMixin, FilterContextMixin, generic.TemplateView):
    template_name = 'training/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['training_filters'] = TrainingFilter.objects.all()
        return context


class SearchView(TrainingListView):
    template_name = 'training/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('suche')
        if search:
            trainings = Training.objects.filter(
                Q(name__icontains=search) | Q(filters__name__icontains=search)
            ).distinct()
            context['trainings'] = trainings
            context['videos_count'] = trainings.count()
        return context


class BookmarksView(TrainingListView):
    template_name = 'training/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trainings = self.request.user.settings.bookmarks.all()
        context['trainings'] = trainings
        context['videos_count'] = trainings.count()
        return context


class TrainingDetailView(LoginRequiredMixin, SettingsContextMixin, FilterContextMixin, generic.DetailView):
    template_name = 'training/detail.html'
    model = Training

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmarked'] = self.request.user.settings.bookmarks.filter(pk=self.object.pk).exists()
        return context


# save settings views
class AgeGroupFormView(UpdateUserSettingsMixin, generic.UpdateView):
    form_class = SelectAgeGroupForm


class DifficultiesFormView(UpdateUserSettingsMixin, generic.UpdateView):
    form_class = SelectDifficultiesForm


# get change views
class BookmarkTrainingView(LoginRequiredMixin, generic.DetailView):
    model = Training

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        bookmarks = list(self.request.user.settings.bookmarks.all())
        if self.object in bookmarks:
            self.request.user.settings.bookmarks.remove(self.object.pk)
        else:
            self.request.user.settings.bookmarks.add(self.object.pk)
        self.request.user.settings.save()
        return HttpResponseRedirect(reverse('training_detail', args=[self.object.pk]))


class ResetAgeGroupView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        self.request.user.settings.age_group = None
        self.request.user.settings.save()
        return HttpResponseRedirect(reverse('training_list'))


class ResetTrainingFiltersView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        self.request.user.settings.training_filters.set([])
        self.request.user.settings.filter_groups.set([])
        self.request.user.settings.save()
        return HttpResponseRedirect(reverse('training_list'))


class ResetDifficultyView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        self.request.user.settings.difficulties.set([])
        self.request.user.settings.save()
        return HttpResponseRedirect(reverse('training_list'))


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
        user_training_filters = request.user.settings.training_filters
        if user_training_filters.filter(pk=pk).exists():
            user_training_filters.remove(pk)
            action = 'removed'
        else:
            user_training_filters.add(pk)
            action = 'added'
        trainings = Training.objects.all()
        for training_filter in list(user_training_filters.all()):
            trainings = trainings.filter(filters=training_filter.pk)
        data = {
            'status': 'ok',
            'action': action,
            'videos': trainings.count()
        }
        return Response(data)
