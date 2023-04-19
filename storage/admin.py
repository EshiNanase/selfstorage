from django.contrib import admin
from django.utils.html import format_html

from .models import Storage, StorageImage, Box


admin.site.register(StorageImage)


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_filter = ['is_stored', 'storage__slug']


class BoxInline(admin.TabularInline):
    model = Box


class StorageImageInline(admin.TabularInline):
    model = StorageImage
    readonly_fields = ['preview_image']

    def preview_image(self, obj):
        return format_html(
            '<img src="{url}" width="200" />'.format(
                url=obj.image.url
            )
        )
    fields = ('image', 'preview_image')


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['city', 'street']}
    inlines = [BoxInline, StorageImageInline]
    fields = (
        'city',
        'street',
        'building',
        'specificity',
        'description',
        'longitude',
        'latitude',
        'slug'
    )
    list_filter = ['city']
