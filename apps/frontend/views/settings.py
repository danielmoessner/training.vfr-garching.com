from django.contrib.auth.mixins import LoginRequiredMixin
from apps.settings.models import Fundamentals
from apps.frontend.views import SettingsContextMixin
from django.views import generic


class FundamentalsView(LoginRequiredMixin, SettingsContextMixin, generic.TemplateView):
    template_name = 'fundamentals.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = Fundamentals.get_solo()
        return context
