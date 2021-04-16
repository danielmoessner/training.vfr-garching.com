from django.db import models

from apps.trainings.models import Filter


class Block(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    and_filters = models.ManyToManyField(Filter, verbose_name='UND Filter', blank=True, related_name='or_blocks')
    or_filters = models.ManyToManyField(Filter, verbose_name='ODER Filter', blank=True, related_name='and_blocks')

    class Meta:
        verbose_name = 'Baustein'
        verbose_name_plural = 'Bausteine'
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)


class Structure(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    block1 = models.ForeignKey(Block, verbose_name='Baustein 1', on_delete=models.PROTECT, blank=True, null=True, related_name='structures1')
    block2 = models.ForeignKey(Block, verbose_name='Baustein 2', on_delete=models.PROTECT, blank=True, null=True, related_name='structures2')
    block3 = models.ForeignKey(Block, verbose_name='Baustein 3', on_delete=models.PROTECT, blank=True, null=True, related_name='structures3')
    block4 = models.ForeignKey(Block, verbose_name='Baustein 4', on_delete=models.PROTECT, blank=True, null=True, related_name='structures4')
    block5 = models.ForeignKey(Block, verbose_name='Baustein 5', on_delete=models.PROTECT, blank=True, null=True, related_name='structures5')
    blocks = models.ManyToManyField(Block, through='StructureBlock')

    class Meta:
        verbose_name = 'Struktur'
        verbose_name_plural = 'Strukturen'
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)


class StructureBlock(models.Model):
    structure = models.ForeignKey(Structure, on_delete=models.CASCADE, verbose_name='Struktur')
    block = models.ForeignKey(Block, on_delete=models.CASCADE, verbose_name='Block')
    order = models.IntegerField(verbose_name='Sortierung')

    class Meta:
        ordering = ['structure', 'order']
        verbose_name = 'Struktur-Block-Verbindung'
        verbose_name_plural = 'Struktur-Block-Verbindungen'

    def __str__(self):
        return '{} - Block {}'.format(self.structure.name, self.order)


class Topic(models.Model):
    name = models.CharField(verbose_name='Name', max_length=80)
    or_filters = models.ManyToManyField(Filter, verbose_name='ODER Filter', blank=True, related_name='topics')

    class Meta:
        verbose_name = 'Thema'
        verbose_name_plural = 'Themen'
        ordering = ['name']

    def __str__(self):
        return '{}'.format(self.name)
