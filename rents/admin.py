from django.contrib import admin
from django.utils.timezone import now

from rents.models import Rent


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    fields = (
        'client',
        'box',
        'box_price',
        'status',
        'started_at',
        'expired_at',
        'closed_at'
    )
    readonly_fields = (
        'box_price',
        'started_at',
        'closed_at'
    )

    def save_form(self, request, form, change):
        instance = form.save(commit=False)
        if not instance.closed_at and instance.status == 'CLOSED':
            instance.closed_at = now()
        if not instance.closed_at and instance.expired_at < now():
            instance.status = 'EXPIRED'

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not change or not instance.box_price:
                instance.box_price = instance.box.price
            instance.save()
        formset.save()
