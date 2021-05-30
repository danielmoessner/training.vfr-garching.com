from solo.models import SingletonModel
from django.db import models


class General(SingletonModel):
    favicon = models.ImageField(upload_to='general/', verbose_name='Favicon')
    meta_title = models.CharField(verbose_name='Meta-Titel', max_length=60)
    meta_description = models.CharField(verbose_name='Meta-Beschreibung', max_length=120)
    meta_image = models.ImageField(upload_to='general/', verbose_name='Meta-Bild')
    link = models.URLField(verbose_name='Ausbildungskonzept-Link', max_length=120)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Allgemein'
        verbose_name_plural = 'Allgemein'

    def __str__(self):
        return 'Allgemein'


class Trainings(SingletonModel):
    step1_heading = models.CharField(verbose_name='Schritt 1 Überschrift', max_length=100)
    step1_info = models.TextField(verbose_name='Schritt 1 Info')
    step2_heading = models.CharField(verbose_name='Schritt 2 Überschrift', max_length=100)
    step2_info = models.TextField(verbose_name='Schritt 2 Info')
    step3_heading = models.CharField(verbose_name='Schritt 3 Überschrift', max_length=100)
    step3_info = models.TextField(verbose_name='Schritt 3 Info')
    step4_heading = models.CharField(verbose_name='Schritt 4 Überschrift', max_length=100)
    step4_info = models.TextField(verbose_name='Schritt 4 Info')
    step5_heading = models.CharField(verbose_name='Schritt 5 Überschrift', max_length=100)
    step5_info = models.TextField(verbose_name='Schritt 5 Info')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Trainings'
        verbose_name_plural = 'Trainings'

    def __str__(self):
        return 'Trainings'


class Fundamentals(SingletonModel):
    heading = models.CharField(verbose_name='Überschrift', max_length=100)
    video1 = models.CharField(verbose_name='Video 1', blank=True, null=True, max_length=600)
    video2 = models.CharField(verbose_name='Video 2', blank=True, null=True, max_length=600)

    class Meta:
        verbose_name = 'Technik-Grundlagen'
        verbose_name_plural = 'Technik-Grundlagen'

    def __str__(self):
        return 'Technik-Grundlagen'

    def get_video1_code(self):
        if self.video1:
            return self.video1.split('/')[-1]
        return ''

    def get_video2_code(self):
        if self.video2:
            return self.video2.split('/')[-1]
        return ''
