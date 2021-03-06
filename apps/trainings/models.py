import json

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
from django.urls import reverse
from tinymce.models import HTMLField
from django.utils import timezone
from django.db import models
from datetime import timedelta
import urllib.parse


class Difficulty(models.Model):
    name = models.CharField(max_length=80, verbose_name='Name')
    ordering = models.IntegerField(verbose_name='Sortierung')
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], verbose_name='Sterne')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Schwierigkeit'
        verbose_name_plural = 'Schwierigkeiten'
        ordering = ['ordering']


class Youth(models.Model):
    name = models.CharField(max_length=80, verbose_name='Name')
    ordering = models.IntegerField(verbose_name='Sortierung', default=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Jugend'
        verbose_name_plural = 'Jugenden'
        ordering = ['ordering']

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        create = False if self.pk else True
        super().save(*args, **kwargs)
        if create:
            for training_filter in Filter.objects.all():
                training_filter.age_groups.add(self)


class Group(models.Model):
    name = models.CharField(max_length=80, verbose_name='Name')
    group = models.ForeignKey('self', verbose_name='Gruppe', null=True, blank=True, on_delete=models.PROTECT,
                              related_name='groups')
    ordering = models.IntegerField(verbose_name='Sortierung')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Filtergruppe'
        verbose_name_plural = 'Filtergruppen'
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
        training_filters = Filter.objects.select_related('group').all()
        if not show_hidden:
            training_filters = training_filters.filter(hide=False)
        if settings and settings.age_group:
            training_filters = training_filters.filter(age_groups=settings.age_group)
        training_filters = list(training_filters)

        for group in list(Group.objects.prefetch_related('training_filters', 'groups').all()):
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


class PlayerAmount(models.Model):
    amount = models.IntegerField('Spieleranzahl')

    class Meta:
        verbose_name = 'Spieleranzahl'
        verbose_name_plural = 'Spieleranzahlen'
        ordering = ['amount']

    def __str__(self):
        return '{}'.format(self.amount)


class Filter(models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name='Gruppe',
                              related_name='training_filters')
    name = models.CharField(max_length=80, verbose_name='Name')
    ordering = models.IntegerField(verbose_name='Sortierung')
    age_groups = models.ManyToManyField(Youth, verbose_name='Altersgruppen', blank=True)
    hide = models.BooleanField(default=False, verbose_name='Versteckt')
    show_on_detail = models.BooleanField(verbose_name='Auf der Detailseite anzeigen', default=False)
    show_on_detail_bottom = models.BooleanField(verbose_name='Auf der Detailseite unten anzeigen', default=False)
    show_on_trainings_generator_step_4 = models.BooleanField(verbose_name='Im Trainingsgenerator Schritt 2 anzeigen',
                                                             default=False)
    show_on_trainings_generator_step_4_row_2 = models.BooleanField(
        verbose_name='Im Trainingsgenerator Schritt 2 anzeigen auf Reihe 2',
        default=False)
    description = models.TextField(verbose_name='Beschreibung', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Filter'
        verbose_name_plural = 'Filter'
        ordering = ['ordering']

    def __str__(self):
        return '{}'.format(self.name)

    def get_group_path(self):
        return self.group.get_group_path()

    def get_detail_html(self):
        return '<b>{}:</b> {}'.format(self.group.name, self.name)

    @staticmethod
    def search(filters, search):
        return filters.filter(name__icontains=search)

    @staticmethod
    def get_filters_dict(settings=None):
        filters = {}
        training_filters = Filter.objects.filter(hide=False)
        if settings and settings.age_group:
            training_filters.filter(age_groups=settings.age_group)
        for training_filter in list(training_filters):
            data = {
                'name': training_filter.name,
            }
            filters[training_filter.pk] = data
        return filters


class Exercise(models.Model):
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
    filters = models.ManyToManyField(Filter, verbose_name='Filter', blank=True, related_name='trainings')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    player_amounts = models.ManyToManyField(PlayerAmount, verbose_name='Spieleranzahlen', blank=True,
                                            related_name='exercises')

    class Meta:
        verbose_name = '??bung'
        verbose_name_plural = '??bungen'
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def new(self):
        if self.created + timedelta(days=30) > timezone.now():
            return True
        return False

    @staticmethod
    def json_all(exercises=None):
        if exercises is None:
            exercises = Exercise.objects.all()
        ret = []
        for exercise in exercises.prefetch_related('filters').select_related('difficulty'):
            ret.append(exercise.json())
        return ret

    def json(self):
        return {
            'created': self.created.strftime('%Y%m%d'),
            'id': self.pk,
            'name': self.name,
            'video': bool(self.video),
            'new': self.new,
            'stars': self.difficulty.stars,
            'difficulty': self.difficulty.name,
            'focus': self.focus,
            'image': self.image1.url,
            'filterNames': [f.name for f in self.filters.all() if f.show_on_detail_bottom],
            'filterIds': [f.id for f in self.filters.all()],
        }

    @staticmethod
    def optimize_queryset(exercises=None):
        if exercises is None:
            exercises = Exercise.objects.order_by('?')
        return (exercises
                .select_related('difficulty')
                .prefetch_related('filters')
                )

    @staticmethod
    def get_trainings_list(settings, trainings=None):
        if trainings is None:
            trainings = Exercise.objects.all()
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

    def get_absolute_url(self):
        return reverse('exercise', args=[self.pk])

    def get_share_url(self):
        part1 = settings.URL
        part2 = self.get_absolute_url()
        return '{}{}'.format(part1, part2)

    def get_whatsapp_url(self):
        return urllib.parse.quote(self.get_share_url())

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

    @staticmethod
    def search(exercises, search):
        return exercises.filter(
            Q(name__icontains=search) |
            Q(filters__name__icontains=search) |
            Q(focus__icontains=search)
        ).distinct()

    @staticmethod
    def get_search_queryset(search, trainings=None):
        if trainings is None:
            trainings = Exercise.objects.all()

        trainings = Exercise.search(trainings, search)
        return trainings

    @staticmethod
    def filter_by_block(exercises, block):
        or_filters = block.or_filters.all()
        and_filters = list(block.and_filters.all())
        if or_filters.count() > 0:
            exercises = exercises.filter(filters__in=or_filters).distinct()
        for training_filter in and_filters:
            exercises = exercises.filter(filters=training_filter)
        exercises = exercises.distinct()
        return exercises

    @staticmethod
    def filter_by_topic_new(exercises, topic):
        filters1 = topic.or_filters_1.all()
        if filters1.count() > 0:
            exercises = exercises.filter(filters__in=filters1).distinct()
        filters2 = topic.or_filters_2.all()
        if filters2.count() > 0:
            exercises = exercises.filter(filters__in=filters2).distinct()
        return exercises

    @staticmethod
    def filter_by_topic(exercises, topic, phase):
        filters = topic.or_filters_1.all()
        if filters.count() > 0:
            exercises = exercises.filter(filters__in=filters).distinct()
        if phase == 'MAIN':
            filters = topic.main_or_filters.all()
        elif phase == 'START':
            filters = topic.start_or_filters.all()
        elif phase == 'END':
            filters = topic.end_or_filters.all()
        else:
            return exercises
        if filters.count() > 0:
            exercises = exercises.filter(filters__in=filters).distinct()
        exercises = exercises.distinct()
        return exercises

    @staticmethod
    def filter_by_topic_and_block(topic, block, phase):
        if block is None or topic is None or phase is None:
            return Exercise.objects.none()
        exercises = Exercise.objects.all()
        exercises = Exercise.filter_by_block(exercises, block)
        exercises = Exercise.filter_by_topic(exercises, topic, phase)
        return exercises
