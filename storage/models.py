from django.core.validators import MinValueValidator
from django.db import models


class Storage(models.Model):
    slug = models.SlugField('Название', blank=True)
    description = models.TextField('Описание', blank=True)
    specificity = models.CharField('Особенность', max_length=100, blank=True)
    city = models.CharField('Город', max_length=50, blank=True)
    street = models.CharField('Улица', max_length=100, blank=True)
    building = models.CharField('Дом/корпус', max_length=20, blank=True)
    longitude = models.FloatField('Долгота', null=True, blank=True)
    latitude = models.FloatField('Широта', null=True, blank=True)

    def __str__(self):
        return f'{self.city}, ул.{self.street}, д.{self.building}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class Box(models.Model):
    number = models.CharField('Номер бокса', max_length=24)
    price = models.DecimalField('Стоимость аренды в сутки', max_digits=10, decimal_places=2)
    is_stored = models.BooleanField('Занято', default=False)
    storage = models.ForeignKey(Storage, related_name='boxes', on_delete=models.CASCADE)
    width = models.IntegerField('Ширина (см)', validators=[MinValueValidator(0)])
    height = models.IntegerField('Высота (см)', validators=[MinValueValidator(0)])
    depth = models.IntegerField('Глубина (см)', validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'


class StorageImage(models.Model):
    image = models.ImageField('Фото склада', blank=True, null=True)
    storage = models.ForeignKey(Storage, related_name='images', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фото склада'
        verbose_name_plural = 'Фото складов'
