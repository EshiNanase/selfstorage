from django.core.validators import MinValueValidator
from django.db import models
from services.geocoder import set_coordinates
from .validators import thumbnail_image_restriction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Storage(models.Model):
    slug = models.SlugField('Название', blank=True)
    description = models.TextField('Описание', blank=True)
    specificity = models.CharField('Особенность', max_length=100, blank=True)
    city = models.CharField('Город', max_length=50, blank=True)
    street = models.CharField('Улица', max_length=100, blank=True)
    building = models.CharField('Дом/корпус', max_length=20, blank=True)
    longitude = models.FloatField('Долгота', null=True, blank=True)
    latitude = models.FloatField('Широта', null=True, blank=True)
    celsius_temperature = models.IntegerField('Температура в Цельсиях', null=True, blank=True)
    thumbnail_image = models.ImageField(
        'Миниатюра',
        validators=[thumbnail_image_restriction],
        null=True,
        blank=True
    )

    def get_free_boxes(self):
        total_boxes = self.boxes.prefetch_related('rents').all()
        return [box for box in total_boxes if not box.rents.filter(status__in=['EXPIRED', 'ACTIVE'])]

    def __str__(self):
        return f'{self.city}, ул.{self.street}, д.{self.building}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class Box(models.Model):
    number = models.CharField('Номер бокса', max_length=24)
    price = models.DecimalField('Стоимость аренды в сутки', max_digits=10, decimal_places=2)
    storage = models.ForeignKey(Storage, related_name='boxes', on_delete=models.CASCADE)
    width = models.IntegerField('Ширина (см)', validators=[MinValueValidator(0)])
    height = models.IntegerField('Высота (см)', validators=[MinValueValidator(0)])
    depth = models.IntegerField('Глубина (см)', validators=[MinValueValidator(0)])

    def __str__(self):
        return f'№{self.number}, {self.storage}'

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    @property
    def is_stored(self):
        active_rents = self.rents.filter(status__in=['EXPIRED', 'ACTIVE'])
        if active_rents:
            return True


class StorageImage(models.Model):
    image = models.ImageField('Фото склада', blank=True, null=True)
    storage = models.ForeignKey(Storage, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f'№{self.id}, {self.storage}'

    class Meta:
        verbose_name = 'Фото склада'
        verbose_name_plural = 'Фото складов'


@receiver(post_save, sender=Storage)
def define_coordinates(sender, instance, **kwargs):

    if not instance.latitude or not instance.longitude:
        instance.latitude, instance.longitude = set_coordinates(instance)
        instance.save()
