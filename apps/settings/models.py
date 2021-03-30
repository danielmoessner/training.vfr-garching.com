from solo.models import SingletonModel
from django.db import models


class General(SingletonModel):
    favicon = models.ImageField(upload_to='general/', verbose_name='Favicon')
    meta_title = models.CharField(verbose_name='Meta-Titel', max_length=60)
    meta_description = models.CharField(verbose_name='Meta-Beschreibung', max_length=120)
    meta_image = models.ImageField(upload_to='general/', verbose_name='Meta-Bild')

    class Meta:
        verbose_name = 'Allgemein'
        verbose_name_plural = 'Allgemein'

    def __str__(self):
        return 'Allgemein'
