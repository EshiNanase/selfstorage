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
            'thumbnail_image': storage.thumbnail_image.url,
            'slug': storage.slug,
            'images': [item.image.url for item in storage.images.all()],
            'avaliable_boxes': [],
            'celsius_temperature': storage.celsius_temperature,
            'boxes_amount': storage.boxes.count,
            'box_min_price': storage.boxes.aggregate(Min('price'))['price__min'],
            'box_max_height': round(storage.boxes.aggregate(Max('height'))['height__max'] / 100, 1)
        }
        avaliable_boxes = [box for box in storage.boxes.all() if not box.is_stored]
        for box in avaliable_boxes:
            box_desc = {
                'number': box.number,
                'price': box.price,
                'width': box.width,
                'height': box.height,
                'depth': box.depth,
                'sq_m_area': round(box.width*box.depth / 100, 1)
            }
            storage_desc['avaliable_boxes'].append(box_desc)

        context['storages'].append(storage_desc)

    return render(request, 'boxes.html', context=context)
