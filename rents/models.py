from datetime import timedelta

from django.db import models
from django.db.models import QuerySet
from django.utils.timezone import now

from personal_account.models import Client
from storage.models import Box


class RentQuerySet(QuerySet):
    def filter_expired(self):
        right_now = now()
        yesterday = right_now - timedelta(days=1)
        return self.filter(expired_at__lte=right_now, warning_sent_at__lt=yesterday).select_related('client')

    def filter_soon_expiring(self):
        right_now = now()
        tomorrow = right_now + timedelta(days=1)
        yesterday = right_now - timedelta(days=1)
        return self.filter(expired_at__lte=tomorrow, warning_sent_at__lt=yesterday).exclude(expired_at__gte=right_now).select_related('client')


class Rent(models.Model):
    ACTIVE = 'ACTIVE'
    CLOSED = 'CLOSED'
    EXPIRED = 'EXPIRED'

    STATUSES = [
        (ACTIVE, 'Активна'),
        (CLOSED, 'Завершена'),
        (EXPIRED, 'Просрочена')
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='rents', verbose_name='Арендатор')
    box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True, related_name='rents', verbose_name='Бокс')
    box_price = models.DecimalField('Стоимость аренды в сутки', max_digits=10, decimal_places=2)
    status = models.CharField('Статус', choices=STATUSES, max_length=20, default='ACTIVE')
    started_at = models.DateTimeField('Начало аренды', default=now)
    expired_at = models.DateTimeField('Окончание аренды')
    closed_at = models.DateTimeField('Завершена', null=True, blank=True)
    warning_sent_at = models.DateTimeField('Предупреждение отправлено', null=True, blank=True)

    objects = RentQuerySet.as_manager()

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
