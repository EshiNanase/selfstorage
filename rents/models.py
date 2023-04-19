from django.db import models
from django.utils.timezone import now

from storage.models import Box


class Rent(models.Model):
    STATUSES = [
        ('ACTIVE', 'Активна'),
        ('CLOSED', 'Завершена'),
        ('EXPIRED', 'Просрочена')
    ]

    box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True, related_name='rents', verbose_name='Бокс')
    status = models.CharField('Статус', choices=STATUSES)
    started_at = models.DateTimeField('Начало аренды', default=now)
    expired_at = models.DateTimeField('Окончание аренды')
    closed_at = models.DateTimeField('Завершён')

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
