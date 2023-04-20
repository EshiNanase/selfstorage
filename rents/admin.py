from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import now

from rents.models import Rent


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    fields = [
        'client',
        'box',
        'box_price',
        'get_total_cost',
        'status',
        'started_at',
        'expired_at',
        'closed_at'
    ]
    list_display = [
        'id',
        'status',
        'box',
        'started_at',
        'expired_at',
    ]
    list_display_links = [
        'id'
    ]
    readonly_fields = [
        'client',
        'box_price',
        'started_at',
        'closed_at',
        'get_total_cost'
    ]

    def get_total_cost(self, obj):
        rent_ended_at = obj.closed_at or obj.expired_at
        time_range = rent_ended_at - obj.started_at
        days = max(1, time_range.days)
        total_cost = days * obj.box_price
        return total_cost

    get_total_cost.short_description = 'Общая стоимость'

    def save_form(self, request, form, change):
        instance = form.save(commit=False)
        if not instance.closed_at and instance.status == 'CLOSED':
            instance.closed_at = now()
        if not instance.closed_at and instance.expired_at < now():
            instance.status = 'EXPIRED'
        if not instance.box_price:
            instance.box_price = instance.box.price
        return form.save()
