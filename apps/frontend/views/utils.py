from django.views.generic.base import ContextMixin
from apps.settings.models import General
from apps.users.models import UserSettings


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
            settings, created = UserSettings.objects.select_related('age_group').prefetch_related(
                'bookmarks').get_or_create(user=self.request.user)
            context['user_settings'] = settings
        return context
