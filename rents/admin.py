from django.contrib import admin
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
    readonly_fields = [
        'box_price',
        'started_at',
        'closed_at',
        'get_total_cost'
    ]
    list_filter = [
        'status',
        'box'
    ]

    def get_total_cost(self, obj):
        rent_ended_at = obj.closed_at or obj.expired_at or now()
        time_range = rent_ended_at - obj.started_at
        days = max(1, time_range.days)
        price = obj.box_price or obj.box.price or 0
        total_cost = days * price
        return total_cost

    get_total_cost.short_description = 'Общая стоимость'

    def save_form(self, request, form, change):
        instance = form.save(commit=False)
        if not instance.closed_at and instance.expired_at < now() and not instance.status == Rent.CLOSED:
            instance.status = 'EXPIRED'
        if not instance.box_price:
            instance.box_price = instance.box.price
        if not instance.closed_at and instance.status == 'CLOSED':
            instance.closed_at = now()
        return form.save()
