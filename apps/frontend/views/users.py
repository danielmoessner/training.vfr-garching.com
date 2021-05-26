from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from apps.users.models import UserSettings
from apps.users.forms import SelectAgeGroupForm, SelectDifficultiesForm, SearchForm
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .utils import SettingsContextMixin, SuccessUrlReverseMixin


# mixins
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


class SettingsView(LoginRequiredMixin, SettingsContextMixin, generic.UpdateView):
    template_name = 'settings.html'
    form_class = SelectAgeGroupForm
    success_url = reverse_lazy('settings')

    def get_object(self, queryset=None):
        return self.request.user.settings

    def form_valid(self, form):
        messages.success(self.request, 'Einstellungen gespeichert.')
        return super().form_valid(form=form)


class AgeGroupFormView(LoginRequiredMixin, SuccessUrlReverseMixin, UpdateUserSettingsMixin, generic.UpdateView):
    form_class = SelectAgeGroupForm


class DifficultiesFormView(LoginRequiredMixin, SuccessUrlReverseMixin, UpdateUserSettingsMixin, generic.UpdateView):
    form_class = SelectDifficultiesForm


class SearchFormView(LoginRequiredMixin, UpdateUserSettingsMixin, generic.UpdateView):
    form_class = SearchForm

    def get_success_url(self):
        return self.request.POST.get('reverse')
