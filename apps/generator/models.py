from django.db import models

from apps.trainings.models import Filter


class Block(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
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

    def get_blocks(self):
        return [self.block1, self.block2, self.block3, self.block4, self.block5]

    def get_block5_exists(self):
        return self.block5.all().exists()


class Topic(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    ordering = models.IntegerField(verbose_name='Sortierung', default=1)
    or_filters = models.ManyToManyField(Filter, verbose_name='HAUPTTEIL ODER Filter', blank=True,
                                        related_name='main_topics')
    warm_up_or_filters = models.ManyToManyField(Filter, verbose_name='WARM-UP ODER Filter', blank=True,
                                                related_name='warm_up_topics')
    structures = models.ManyToManyField(Structure, blank=True, verbose_name='Strukturen')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Thema'
        verbose_name_plural = 'Themen'
        ordering = ['ordering']

    def __str__(self):
        return '{}'.format(self.name)
