from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import ContextMixin
from rest_framework.response import Response
from apps.trainings.models import Training, FilterGroup, TrainingFilter, AgeGroup
from apps.settings.models import General
from rest_framework.views import APIView
from apps.users.models import UserSettings
from apps.users.forms import SelectAgeGroupForm
from django.views import generic


class SettingsContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = General.get_solo()
        return context


class LoginView(SettingsContextMixin, DjangoLoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    redirect_field_name = 'next'


class LogoutView(DjangoLogoutView):
    pass


class FilterContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings, created = UserSettings.objects.get_or_create(user=self.request.user)
        context['groups'] = FilterGroup.get_groups_dict(settings=settings)
        context['root_group_pks'] = [group.pk for group in FilterGroup.objects.filter(group=None)]
        context['age_group_form'] = SelectAgeGroupForm(instance=settings)
        context['trainings'] = Training.objects.all()
        context['groups_open'] = self.request.user.settings.get_filter_groups()
        context['filters_selected'] = self.request.user.settings.get_training_filters()
        trainings = Training.objects.all()
        for training_filter in list(self.request.user.settings.training_filters.all()):
            trainings = trainings.filter(filters=training_filter.pk)
        context['videos_count'] = trainings.count()
        return context


class UpdateUserSettingsMixin:
    def post(self, request, *args, **kwargs):
        settings, created = UserSettings.objects.get_or_create(user=self.request.user)
        form = SelectAgeGroupForm(instance=settings, data=self.request.POST)
        if form.is_valid():
            form.save()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class TrainingListView(LoginRequiredMixin, SettingsContextMixin, UpdateUserSettingsMixin, FilterContextMixin, generic.TemplateView):
    template_name = 'training/list.html'


class TrainingDetailView(LoginRequiredMixin, SettingsContextMixin, UpdateUserSettingsMixin, FilterContextMixin, generic.DetailView):
    template_name = 'training/detail.html'
    model = Training

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class ResetAgeGroupView(LoginRequiredMixin, generic.View):
    def get(self, request):
        self.request.user.settings.age_group = None
        self.request.user.settings.save()
        return HttpResponseRedirect(reverse('training_list'))


class ResetTrainingFiltersView(LoginRequiredMixin, generic.View):
    def get(self, request):
        self.request.user.settings.training_filters.set([])
        self.request.user.settings.filter_groups.set([])
        self.request.user.settings.save()
        return HttpResponseRedirect(reverse('training_list'))


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
