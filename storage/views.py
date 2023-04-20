from django.shortcuts import render
from django.db.models import Min, Max

from .models import Storage, Box


def faq(request):
    return render(request, 'faq.html')


def index(request):
    return render(request, 'index.html')


def boxes(request):
    storages = Storage.objects.all()
    context = {
        'storages': []
    }

    for storage in storages:
        
        storage_desc = {
            'description': storage.description,
            'specificity': storage.specificity,
            'city': storage.city,
            'street': storage.street,
            'building': storage.building,
            'slug': storage.slug,
            'images': [item.image.url for item in storage.images.all()],
            'avaliable_boxes': [],
            'boxes_amount': storage.boxes.count,
            'box_min_price': storage.boxes.aggregate(Min('price'))['price__min'],
            'box_max_height': round(storage.boxes.aggregate(Max('height'))['height__max'] / 100, 1)
        }
        context['storages'].append(storage_desc)

    return render(request, 'boxes.html', context=context)
