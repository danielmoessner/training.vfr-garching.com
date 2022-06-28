from apps.trainings.models import Filter, Exercise, Youth, PlayerAmount
from django.db.models import Prefetch
from django.conf import settings
from django.urls import reverse
from django.db import models
import urllib.parse


class Block(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    description = models.TextField(verbose_name='Beschreibung')
    ordering = models.IntegerField(verbose_name='Sortierung', default=1)
    and_filters = models.ManyToManyField(Filter, verbose_name='UND Filter', blank=True, related_name='or_blocks')
    or_filters = models.ManyToManyField(Filter, verbose_name='ODER Filter', blank=True, related_name='and_blocks')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Baustein'
        verbose_name_plural = 'Bausteine'
        ordering = ['ordering']

    def __str__(self):
        return '{}'.format(self.name)


class Structure(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    ordering = models.IntegerField(verbose_name='Sortierung', default=1)
    PHASE_CHOICES = (
        ('START', 'Warm-Up'),
        ('MAIN', 'Hauptteil'),
        ('END', 'Abschluss')
    )
    blocks1 = models.ManyToManyField(Block, verbose_name='Baustein 1', related_name='structures1')
    phase1 = models.CharField(verbose_name='Baustein 1 Phase', choices=PHASE_CHOICES, max_length=50)
    blocks2 = models.ManyToManyField(Block, verbose_name='Baustein 2', related_name='structures2')
    phase2 = models.CharField(verbose_name='Baustein 2 Phase', choices=PHASE_CHOICES, max_length=50)
    blocks3 = models.ManyToManyField(Block, verbose_name='Baustein 3', related_name='structures3')
    phase3 = models.CharField(verbose_name='Baustein 3 Phase', choices=PHASE_CHOICES, max_length=50)
    blocks4 = models.ManyToManyField(Block, verbose_name='Baustein 4', related_name='structures4')
    phase4 = models.CharField(verbose_name='Baustein 4 Phase', choices=PHASE_CHOICES, max_length=50)
    blocks5 = models.ManyToManyField(Block, verbose_name='Baustein 5', related_name='structures5', blank=True)
    phase5 = models.CharField(verbose_name='Baustein 5 Phase', choices=PHASE_CHOICES, max_length=50, blank=True,
                              null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Struktur'
        verbose_name_plural = 'Strukturen'
        ordering = ['ordering']

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def blocks(self):
        data = {}
        for i in range(1, 6):
            phase = getattr(self, 'get_phase{}_display'.format(i))
            blocks = getattr(self, 'blocks{}'.format(i))
            if blocks and phase:
                data[i] = (phase(), blocks.all())
        return data

    def get_blocks(self):
        data = []
        for i in range(1, 6):
            phase = getattr(self, 'get_phase{}_display'.format(i))
            blocks = getattr(self, 'blocks{}'.format(i))
            if blocks and phase:
                data.append((phase(), blocks.all()))
        return data


class Group(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    ordering = models.IntegerField(verbose_name='Sortierung')

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Gruppe'
        verbose_name_plural = 'Gruppen'

    def __str__(self):
        return self.name

    @staticmethod
    def optimize_queryset(groups=None, user_settings=None):
        if groups is None:
            groups = Group.objects.all()
        topics = Topic.objects.all()
        if user_settings and user_settings.age_group:
            topics = topics.filter(youths=user_settings.age_group)
        return groups.prefetch_related(Prefetch('topics', queryset=topics)).all()


class Topic(models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, related_name='topics')
    pre = models.CharField(verbose_name='Pre', max_length=80)
    name = models.CharField(verbose_name='Name', max_length=80)
    description = models.TextField(verbose_name='Beschreibung')
    ordering = models.IntegerField(verbose_name='Sortierung', default=1)
    youths = models.ManyToManyField(Youth, related_name='topics', verbose_name='Jugenden', blank=True)
    # structures = models.ManyToManyField(Structure, blank=True, verbose_name='Strukturen')
    or_filters_1 = models.ManyToManyField(Filter, verbose_name='ALLGEMEINE ODER Filter', blank=True,
                                          related_name='general_topics')
    or_filters_2 = models.ManyToManyField(Filter, verbose_name='ALTERSGRUPPE ODER Filter', blank=True)
    # start_or_filters = models.ManyToManyField(Filter, verbose_name='WARM-UP ODER Filter', blank=True,
    #                                           related_name='start_topics')
    # main_or_filters = models.ManyToManyField(Filter, verbose_name='HAUPTTEIL ODER Filter', blank=True,
    #                                          related_name='main_topics')
    # end_or_filters = models.ManyToManyField(Filter, verbose_name='ABSCHLUSS ODER Filter', blank=True,
    #                                         related_name='end_topic')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Thema'
        verbose_name_plural = 'Themen'
        ordering = ['ordering']

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def full_name(self):
        return '{}: {}'.format(self.pre, self.name)


class Training(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    description = models.TextField(verbose_name='Beschreibung', blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='trainings',
                              blank=True, null=True, verbose_name='Thema')
    player_amount = models.ForeignKey(PlayerAmount, verbose_name='Spieleranzahl', blank=True, null=True,
                                      on_delete=models.SET_NULL)
    AMOUNT_CHOICES = (
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    exercise_amount = models.CharField(verbose_name='Übungsanzahl', max_length=1, choices=AMOUNT_CHOICES, blank=True,
                                       null=True)
    # structure = models.ForeignKey(Structure, on_delete=models.PROTECT, related_name='trainings',
    #                               blank=True, null=True, verbose_name='Trainingsstruktur')
    exercise1 = models.ForeignKey(Exercise, on_delete=models.PROTECT, related_name='trainings1', verbose_name='Übung 1',
                                  blank=True, null=True)
    # block1 = models.ForeignKey(Block, on_delete=models.SET_NULL, related_name='trainings1',
    #                            verbose_name='Block 1', blank=True, null=True)
    exercise2 = models.ForeignKey(Exercise, on_delete=models.PROTECT, related_name='trainings2', verbose_name='Übung 2',
                                  blank=True, null=True)
    # block2 = models.ForeignKey(Block, on_delete=models.SET_NULL, related_name='trainings2',
    #                            verbose_name='Block 2', blank=True, null=True)
    exercise3 = models.ForeignKey(Exercise, on_delete=models.PROTECT, related_name='trainings3', verbose_name='Übung 3',
                                  blank=True, null=True)
    # block3 = models.ForeignKey(Block, on_delete=models.SET_NULL, related_name='trainings3',
    #                            verbose_name='Block 3', blank=True, null=True)
    exercise4 = models.ForeignKey(Exercise, on_delete=models.PROTECT, related_name='trainings4', verbose_name='Übung 4',
                                  blank=True, null=True)
    # block4 = models.ForeignKey(Block, on_delete=models.SET_NULL, related_name='trainings4',
    #                            verbose_name='Block 4', blank=True, null=True)
    exercise5 = models.ForeignKey(Exercise, on_delete=models.PROTECT, related_name='trainings5', verbose_name='Übung 5',
                                  blank=True, null=True)
    # block5 = models.ForeignKey(Block, on_delete=models.SET_NULL, related_name='trainings5',
    #                            verbose_name='Block 5', blank=True, null=True)
    user = models.ForeignKey('users.UserSettings', on_delete=models.PROTECT, related_name='trainings',
                             verbose_name='Nutzer', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Training'
        verbose_name_plural = 'Trainings'
        ordering = ['user', '-created']

    def __str__(self):
        name = '{}'.format(self.name)
        if not self.user:
            return name
        return 'VfR Training: {}'.format(name)

    @staticmethod
    def optimize_queryset(trainings=None):
        if trainings is None:
            trainings = Training.objects.all()
        return trainings.select_related('topic',
                                        # 'structure',
                                        'exercise1', 'exercise2', 'exercise3', 'exercise4', 'exercise5',
                                        # 'block1', 'block2', 'block3', 'block4', 'block5',
                                        'exercise1__difficulty', 'exercise2__difficulty', 'exercise3__difficulty',
                                        'exercise4__difficulty', 'exercise5__difficulty',
                                        )

    @staticmethod
    def get_remaining_fields(all_except):
        fields = ['name', 'description', 'topic', 'player_amount', 'exercise_amount',
                  # 'structure',
                  # 'block1', 'block2', 'block3', 'block4', 'block5',
                  'exercise1', 'exercise2', 'exercise3', 'exercise4', 'exercise5']
        fields = list(filter(lambda field: field not in all_except, fields))
        return fields

    def get_exercise_pk(self, number):
        exercise = getattr(self, 'exercise{}'.format(number), None)
        if exercise:
            return exercise.pk
        return ''

    def get_block_pk(self, number):
        return ''

    def get_structure_pk(self):
        return ''

    def get_topic_pk(self):
        if self.topic:
            return self.topic.pk
        return ''

    def get_base_url_infos(self):
        part1 = '?topic={}&structure={}'.format(self.get_topic_pk(),
                                                self.get_structure_pk())
        part2 = '&block1={}&block2={}&block3={}&block4={}&block5={}'.format(self.get_block_pk(1),
                                                                            self.get_block_pk(2),
                                                                            self.get_block_pk(3),
                                                                            self.get_block_pk(4),
                                                                            self.get_block_pk(5))
        part3 = '&exercise1={}&exercise2={}&exercise3={}&exercise4={}&exercise5={}'.format(self.get_exercise_pk(1),
                                                                                           self.get_exercise_pk(2),
                                                                                           self.get_exercise_pk(3),
                                                                                           self.get_exercise_pk(4),
                                                                                           self.get_exercise_pk(5))
        part4 = '&name={}&description={}'.format(urllib.parse.quote(self.name), urllib.parse.quote(self.description))
        return '{}{}{}{}'.format(part1, part2, part3, part4)

    def get_whatsapp_url(self):
        part1 = settings.URL
        part2 = '{}'.format(reverse('training'))
        part3 = self.get_base_url_infos()
        url = '{}{}{}'.format(part1, part2, part3)
        return urllib.parse.quote(url)

    def get_share_url(self):
        part1 = settings.URL
        part2 = '{}'.format(reverse('training'))
        part3 = self.get_base_url_infos()
        url = '{}{}{}'.format(part1, part2, part3)
        return url

    def get_edit_url(self):
        part1 = '{}'.format(reverse('generator'))
        part2 = self.get_base_url_infos()
        part3 = '&training={}'.format(self.pk)
        part4 = '&step=4&exercise_step=1'
        return '{}{}{}{}'.format(part1, part2, part3, part4)

    def get_print_url(self):
        part1 = reverse('training_print')
        part2 = self.get_base_url_infos()
        return '{}{}'.format(part1, part2)


class TrainingGroup(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    trainings = models.ManyToManyField(Training, blank=True)

    class Meta:
        verbose_name = 'Trainingsgruppe'
        verbose_name_plural = 'Trainingsgruppen'

    def __str__(self):
        return self.name
