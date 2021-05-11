from django.contrib.auth.models import User as DjangoUser
from apps.trainings.models import Youth, Group, Filter, Difficulty, Exercise
from django.db import models


def get_difficulties_default():
    return list(Difficulty.objects.all())


class UserSettings(models.Model):
    user = models.OneToOneField(DjangoUser, related_name='settings', on_delete=models.CASCADE,
                                verbose_name='Benutzer')
    age_group = models.ForeignKey(Youth, related_name='users', on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name='Altersgruppe', help_text='Diese Einstellung schränkt die angezeigten Trainings ein.')
    filter_groups = models.ManyToManyField(Group, related_name='users', blank=True, verbose_name='Geöffnete Gruppen')
    training_filters = models.ManyToManyField(Filter, related_name='users', blank=True, verbose_name='Gesetzte Filter')
    difficulties = models.ManyToManyField(Difficulty, related_name='users', blank=True,
                                          default=get_difficulties_default, verbose_name='Schwierigkeit')
    bookmarks = models.ManyToManyField(Exercise, related_name='users', blank=True, verbose_name='Gesetzte Favoriten')
    search = models.CharField(verbose_name='Suche', blank=True, max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Benutzereinstellung'
        verbose_name_plural = 'Benutzereinstellungen'

    def __str__(self):
        return 'Einstellungen für Nutzer: {}'.format(self.user.username)

    def get_filter_groups(self):
        return [item[0] for item in list(self.filter_groups.values_list('pk'))]

    def get_training_filters(self):
        return [item[0] for item in list(self.training_filters.values_list('pk'))]
