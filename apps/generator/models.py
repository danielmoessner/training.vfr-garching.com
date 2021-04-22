from django.db import models

from apps.trainings.models import Filter


class Block(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    and_filters = models.ManyToManyField(Filter, verbose_name='UND Filter', blank=True, related_name='or_blocks')
    or_filters = models.ManyToManyField(Filter, verbose_name='ODER Filter', blank=True, related_name='and_blocks')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Baustein'
        verbose_name_plural = 'Bausteine'
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)


class Structure(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    PHASE_CHOICES = (
        ('START', 'Warm-Up'),
        ('MAIN', 'Hauptteil'),
        ('END', 'Abschluss')
    )
    block1 = models.ForeignKey(Block, verbose_name='Baustein 1', on_delete=models.PROTECT, blank=True, null=True,
                               related_name='structures1')
    phase1 = models.CharField(verbose_name='Baustein 1 Phase', choices=PHASE_CHOICES, max_length=50, blank=True,
                              null=True)
    block2 = models.ForeignKey(Block, verbose_name='Baustein 2', on_delete=models.PROTECT, blank=True, null=True,
                               related_name='structures2')
    phase2 = models.CharField(verbose_name='Baustein 2 Phase', choices=PHASE_CHOICES, max_length=50, blank=True,
                              null=True)
    block3 = models.ForeignKey(Block, verbose_name='Baustein 3', on_delete=models.PROTECT, blank=True, null=True,
                               related_name='structures3')
    phase3 = models.CharField(verbose_name='Baustein 3 Phase', choices=PHASE_CHOICES, max_length=50, blank=True,
                              null=True)
    block4 = models.ForeignKey(Block, verbose_name='Baustein 4', on_delete=models.PROTECT, blank=True, null=True,
                               related_name='structures4')
    phase4 = models.CharField(verbose_name='Baustein 4 Phase', choices=PHASE_CHOICES, max_length=50, blank=True,
                              null=True)
    block5 = models.ForeignKey(Block, verbose_name='Baustein 5', on_delete=models.PROTECT, blank=True, null=True,
                               related_name='structures5')
    phase5 = models.CharField(verbose_name='Baustein 5 Phase', choices=PHASE_CHOICES, max_length=50, blank=True,
                              null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Struktur'
        verbose_name_plural = 'Strukturen'
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)

    def get_blocks(self):
        return [self.block1, self.block2, self.block3, self.block4, self.block5]


class Topic(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    or_filters = models.ManyToManyField(Filter, verbose_name='ODER Filter', blank=True, related_name='topics')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Thema'
        verbose_name_plural = 'Themen'
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)
