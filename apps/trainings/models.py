from django.core.validators import MinValueValidator, MaxValueValidator
from tinymce.models import HTMLField
from django.utils import timezone
from django.db import models
from datetime import timedelta


class Difficulty(models.Model):
    name = models.CharField(max_length=80, verbose_name='Name')
    ordering = models.IntegerField(verbose_name='Sortierung')
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], verbose_name='Sterne')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Schwierigkeit'
        verbose_name_plural = 'Schwierigkeiten'
        ordering = ['ordering']


class AgeGroup(models.Model):
    name = models.CharField(max_length=80, verbose_name='Name')
    ordering = models.IntegerField(verbose_name='Sortierung', default=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Altersgruppe'
        verbose_name_plural = 'Altersgruppen'
        ordering = ['ordering']

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        create = False if self.pk else True
        super().save(*args, **kwargs)
        if create:
            for training_filter in TrainingFilter.objects.all():
                training_filter.age_groups.add(self)


class FilterGroup(models.Model):
    name = models.CharField(max_length=80, verbose_name='Name')
    group = models.ForeignKey('self', verbose_name='Gruppe', null=True, blank=True, on_delete=models.PROTECT,
                              related_name='groups')
    ordering = models.IntegerField(verbose_name='Sortierung')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Gruppe'
        verbose_name_plural = 'Gruppen'
        ordering = ['ordering']

    def __str__(self):
        return '{}'.format(self.name)

    def get_group_path(self):
        if self.group is None:
            return self.name
        else:
            return '{} / {}'.format(self.group.get_group_path(), self.name)

    def get_training_filter_keys(self):
        training_filters = self.training_filters.all()
        return ['filters_{}'.format(training_filter.pk) for training_filter in training_filters]

    def get_groups(self):
        return self.groups.all()

    @staticmethod
    def get_groups_dict(settings=None, show_hidden=False):
        groups = {}
        training_filters = TrainingFilter.objects.select_related('group').all()
        if not show_hidden:
            training_filters = training_filters.filter(hide=False)
        if settings and settings.age_group:
            training_filters = training_filters.filter(age_groups=settings.age_group)
        training_filters = list(training_filters)

        for group in list(FilterGroup.objects.prefetch_related('training_filters', 'groups').all()):
            group_filters = list(filter(lambda training_filter: training_filter.group.id == group.id, training_filters))
            data = {
                'name': group.name,
                'training_filters': [{'pk': training_filter.pk, 'name': training_filter.name} for training_filter in
                                     group_filters],
                'trainingfilters': [item.pk for item in group_filters],
                'subgroups': [subgroup.pk for subgroup in group.groups.all()],
            }
            groups[group.pk] = data
        return groups


class TrainingFilter(models.Model):
    group = models.ForeignKey(FilterGroup, on_delete=models.PROTECT, verbose_name='Gruppe',
                              related_name='training_filters')
    name = models.CharField(max_length=80, verbose_name='Name')
    ordering = models.IntegerField(verbose_name='Sortierung')
    age_groups = models.ManyToManyField(AgeGroup, verbose_name='Altersgruppen', blank=True)
    hide = models.BooleanField(default=False, verbose_name='Versteckt')
    show_on_detail = models.BooleanField(verbose_name='Auf der Detailseite anzeigen', default=False)
    description = models.TextField(verbose_name='Beschreibung', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Filter'
        verbose_name_plural = 'Filter'
        ordering = ['ordering']

    def __str__(self):
        if self.hide:
            return 'Versteckt: {}'.format(self.name)
        return '{}'.format(self.name)

    def get_group_path(self):
        return self.group.get_group_path()

    def get_detail_html(self):
        return '<b>{}:</b> {}'.format(self.group.name, self.name)

    @staticmethod
    def get_filters_dict(settings=None):
        filters = {}
        training_filters = TrainingFilter.objects.filter(hide=False)
        if settings and settings.age_group:
            training_filters.filter(age_groups=settings.age_group)
        for training_filter in list(training_filters):
            data = {
                'name': training_filter.name,
            }
            filters[training_filter.pk] = data
        return filters


class Training(models.Model):
    name = models.CharField(max_length=80, verbose_name='Name')
    difficulty = models.ForeignKey(Difficulty, verbose_name='Schwierigkeit', null=True, on_delete=models.PROTECT)
    focus = models.CharField(max_length=50, verbose_name='Fokus', blank=True)
    description = HTMLField(verbose_name='Beschreibung', null=True, blank=True)
    coaching = HTMLField(verbose_name='Coachingpunkte', null=True, blank=True)
    variations = HTMLField(verbose_name='Variationen', null=True, blank=True)
    image1 = models.ImageField(upload_to='training/', verbose_name='Bild')
    image2 = models.ImageField(upload_to='training/', verbose_name='Bild', null=True, blank=True)
    image3 = models.ImageField(upload_to='training/', verbose_name='Bild', null=True, blank=True)
    image4 = models.ImageField(upload_to='training/', verbose_name='Bild', null=True, blank=True)
    video = models.CharField(verbose_name='Video', blank=True, null=True, max_length=600)
    filters = models.ManyToManyField(TrainingFilter, verbose_name='Filter', blank=True, related_name='trainings')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Training'
        verbose_name_plural = 'Trainings'
        ordering = ['-created']

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def new(self):
        if self.created + timedelta(days=30) > timezone.now():
            return True
        return False

    @staticmethod
    def get_trainings_list(settings, trainings=None):
        if trainings is None:
            trainings = Training.objects.all()
        trainings = (trainings
                     .filter(difficulty__in=settings.difficulties.all())
                     .select_related('difficulty')
                     .prefetch_related('filters'))
        trainings_list = []
        for training in list(trainings):
            data = {
                "pk": training.pk,
                "name": training.name,
                "image1": training.image1,
                "difficulty": training.difficulty,
                "new": training.new,
                "video": bool(training.video),
                "focus": training.focus,
                "filters": [training_filter.pk for training_filter in training.filters.all()]
            }
            trainings_list.append(data)
        return trainings_list

    def get_video_code(self):
        if self.video:
            return self.video.split('/')[-1]
        return ''

    def get_filter_pks(self):
        return [item[0] for item in list(self.get_filters().values_list('pk'))]

    def get_filters(self):
        return self.filters.filter(hide=False)

    def get_detail_filters(self):
        return self.filters.filter(show_on_detail=True)
