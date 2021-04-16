from django.contrib.auth.models import User as DjangoUser
from apps.trainings.models import Youth, Group, Filter, Difficulty, Exercise
from django.db import models


def get_difficulties_default():
    return list(Difficulty.objects.all())


class UserSettings(models.Model):
    user = models.OneToOneField(DjangoUser, related_name='settings', on_delete=models.CASCADE)
    age_group = models.ForeignKey(Youth, related_name='users', on_delete=models.SET_NULL, null=True, blank=True)
    filter_groups = models.ManyToManyField(Group, related_name='users', blank=True)
    training_filters = models.ManyToManyField(Filter, related_name='users', blank=True)
    difficulties = models.ManyToManyField(Difficulty, related_name='users', blank=True,
                                          default=get_difficulties_default)
    bookmarks = models.ManyToManyField(Exercise, related_name='users', blank=True)
    search = models.CharField(verbose_name='Suche', blank=True, max_length=100)

    class Meta:
        verbose_name = 'Benutzereinstellung'
        verbose_name_plural = 'Benutzereinstellungen'

    def __str__(self):
        return 'Einstellungen für Nutzer: {}'.format(self.user.username)

    def get_filter_groups(self):
        return [item[0] for item in list(self.filter_groups.values_list('pk'))]

    def get_training_filters(self):
        return [item[0] for item in list(self.training_filters.values_list('pk'))]
