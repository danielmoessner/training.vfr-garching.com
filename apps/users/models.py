from django.contrib.auth.models import User as DjangoUser
from apps.trainings.models import AgeGroup, FilterGroup, TrainingFilter, Difficulty, Training
from django.db import models


class UserSettings(models.Model):
    user = models.OneToOneField(DjangoUser, related_name='settings', on_delete=models.CASCADE)
    age_group = models.ForeignKey(AgeGroup, related_name='users', on_delete=models.SET_NULL, null=True, blank=True)
    filter_groups = models.ManyToManyField(FilterGroup, related_name='users', blank=True)
    training_filters = models.ManyToManyField(TrainingFilter, related_name='users', blank=True)
    difficulties = models.ManyToManyField(Difficulty, related_name='users', blank=True)
    bookmarks = models.ManyToManyField(Training, related_name='users', blank=True)

    class Meta:
        verbose_name = 'Benutzereinstellung'
        verbose_name_plural = 'Benutzereinstellungen'

    def __str__(self):
        return 'Einstellungen für Nutzer: {}'.format(self.user.username)

    def get_filter_groups(self):
        return [item[0] for item in list(self.filter_groups.values_list('pk'))]

    def get_training_filters(self):
        return [item[0] for item in list(self.training_filters.values_list('pk'))]
