from django.db import models


class Storage(models.Model):
    title = models.CharField('Название', max_length=200),
    description = models.TextField('Описание', null=True, blank=True)
    address = models.CharField('Адрес', max_length=200),
    longitude = models.FloatField('Долгота', null=True, blank=True)
    latitude = models.FloatField('Широта', null=True, blank=True)

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class Box(models.Model):
    number = models.CharField('Номер бокса', max_length=24)
    price = models.DecimalField('Стоимость аренды в сутки', max_digits=10, decimal_places=2)
    is_stored = models.BooleanField('Занято', default=False)
    storage = models.ForeignKey(Storage, related_name='boxes', on_delete=models.CASCADE)
    width = models.IntegerField('Ширина (см)')
    height = models.IntegerField('Высота (см)')
    depth = models.IntegerField('Глубина (см)')

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'
