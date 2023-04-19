from django.db import models
from django.utils.timezone import now

from personal_account.models import Client
from storage.models import Box


class Rent(models.Model):
    STATUSES = [
        ('ACTIVE', 'Активна'),
        ('CLOSED', 'Завершена'),
        ('EXPIRED', 'Просрочена')
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='rents', verbose_name='Арендатор')
    box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True, related_name='rents', verbose_name='Бокс')
    box_price = models.DecimalField('Стоимость аренды в сутки', max_digits=10, decimal_places=2)
    status = models.CharField('Статус', choices=STATUSES, max_length=20)
    started_at = models.DateTimeField('Начало аренды', default=now)
    expired_at = models.DateTimeField('Окончание аренды')
    closed_at = models.DateTimeField('Завершена')

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
