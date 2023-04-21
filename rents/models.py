from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet, Q
from django.utils.timezone import now

from personal_account.models import Client
from storage.models import Box


def one_month_from_today():
    return now() + timedelta(days=30)


class RentQuerySet(QuerySet):
    def filter_expired(self):
        right_now = now()
        yesterday = right_now - timedelta(days=1)
        return self.filter(
            Q(expired_at__lte=right_now),
            Q(closed_at__isnull=True),
            Q(warning_sent_at__lt=yesterday) | Q(warning_sent_at__isnull=True)). \
            select_related('client')

    def filter_soon_expiring(self):
        right_now = now()
        tomorrow = right_now + timedelta(days=1)
        yesterday = right_now - timedelta(days=1)
        return self.filter(
            Q(expired_at__lte=tomorrow),
            Q(expired_at__gte=right_now),
            Q(closed_at__isnull=True),
            Q(warning_sent_at__lt=yesterday) | Q(warning_sent_at__isnull=True)). \
            select_related('client')

    def filter_active(self, client):
        rents = self.filter(client__id=client.id, status__in=[Rent.EXPIRED, Rent.ACTIVE]).select_related('client')
        for rent in rents:
            rent.expire_soon = rent.expired_at < now() + timedelta(days=1)
        return rents


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
    expired_at = models.DateTimeField('Окончание аренды', default=one_month_from_today)
    closed_at = models.DateTimeField('Завершена', null=True, blank=True)
    warning_sent_at = models.DateTimeField('Предупреждение отправлено', null=True, blank=True)

    objects = RentQuerySet.as_manager()

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'

    def __str__(self):
        return f'Рента {self.id}'

    def clean(self):
        box = Box.objects.filter(pk=self.box.id).prefetch_related('rents').first()
        active_rents = box.rents.filter(status__in=[Rent.EXPIRED, Rent.ACTIVE])
        if active_rents and self not in active_rents and self.status != Rent.CLOSED:
            raise ValidationError('Данный бокс занят')
