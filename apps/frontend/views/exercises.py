from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin
from rest_framework.response import Response
from django.template.loader import render_to_string
from apps.trainings.models import Exercise, Group, Filter
from rest_framework.views import APIView
from apps.users.models import UserSettings
from apps.users.forms import SelectAgeGroupForm, SelectDifficultiesForm
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from weasyprint import HTML, CSS
from .utils import SettingsContextMixin, SuccessUrlReverseMixin


# mixins
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


# views
class ExerciseListView(LoginRequiredMixin, SettingsContextMixin, FilterContextMixin, generic.TemplateView):
    template_name = 'exercises.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # trainings
        exercises = Exercise.objects.order_by('?')
        if context['user_settings'].search:
            exercises = Exercise.get_search_queryset(context['user_settings'].search, exercises)
        context['exercises'] = Exercise.optimize_queryset(exercises)
        # count
        for training_filter in list(self.request.user.settings.training_filters.all()):
            exercises = exercises.filter(filters=training_filter.pk)
        context['trainings_count'] = exercises.count()
        # endpoint
        context['endpoint'] = '/api/exercises/'
        # return
        return context


class BookmarksView(ExerciseListView):
    template_name = 'exercises.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookmarked_trainings = self.request.user.settings.bookmarks.all()
        if context['user_settings'].search:
            bookmarked_trainings = Exercise.get_search_queryset(context['user_settings'].search, bookmarked_trainings)
        context['exercises'] = Exercise.optimize_queryset(bookmarked_trainings)
        context['trainings_count'] = '"?"'
        # endpoint
        context['endpoint'] = '/api/bookmarked_exercises/'
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
        # import logging
        # import os
        #
        # logger = logging.getLogger('weasyprint')
        # logger.handlers = []  # Remove the default stderr handler
        # logger.addHandler(logging.FileHandler(os.path.join(settings.BASE_DIR, 'tmp/weasyprint.log')))

        rendered = render_to_string(self.template_name, context)
        # return HttpResponse(content=rendered)
        html = HTML(string=rendered, base_url=self.request.build_absolute_uri())
        # path = os.path.join(settings.BASE_DIR, 'static/dist/css/main.css')
        # print(path)

        pdf = html.write_pdf()
        response = HttpResponse(pdf)
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(self.object.name)
        return response


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


class ResetTrainingFiltersView(LoginRequiredMixin, SuccessUrlReverseMixin, generic.View):
    success_url = reverse_lazy('exercises')

    def get(self, request, *args, **kwargs):
        self.request.user.settings.training_filters.set([])
        self.request.user.settings.filter_groups.set(Group.objects.filter(group=None))
        self.request.user.settings.save()
        return HttpResponseRedirect(self.get_success_url())


# api views
class ExercisesApiView(APIView):
    http_method_names = ['head', 'get']

    def get(self, request):
        if request.user.settings.search:
            all_exercises = Exercise.objects.all()
            exercises = Exercise.get_search_queryset(request.user.settings.search, all_exercises)
            data = Exercise.json_all(exercises)
        else:
            data = Exercise.json_all()
        return Response(data)


class BookmarkedExercisesApiView(APIView):
    http_method_names = ['head', 'get']

    def get(self, request):
        return Response(Exercise.json_all(request.user.settings.bookmarks.all()))


class ToggleFilterGroupApiView(APIView):
    http_method_names = ['head', 'post']

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
    http_method_names = ['head', 'post']

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
    http_method_names = ['head', 'get']

    def get(self, request):
        search = request.GET.get('search', default='')
        if search:
            exercises = Exercise.search(Exercise.objects.all(), search)[:5]
            exercises = [{'name': result.name, 'type': 'EXERCISE', 'focus': result.focus} for result in exercises]
            filters = Filter.search(Filter.objects.filter(hide=False), search)[:5]
            filters = [{'name': result.name, 'type': 'FILTER'} for result in filters]
            results = {'exercises': exercises, 'filters': filters}
            data = results
        else:
            data = {'exercises': [], 'filters': []}
        return Response(data)


class BookmarkApiView(APIView):
    http_method_names = ['head', 'post']

    def post(self, request, pk=None):
        if self.request.user.settings.bookmarks.filter(pk=pk).exists():
            self.request.user.settings.bookmarks.remove(pk)
            action = 'removed'
        else:
            self.request.user.settings.bookmarks.add(pk)
            action = 'added'
        data = {
            'status': 'ok',
            'action': action
        }
        return Response(data)
