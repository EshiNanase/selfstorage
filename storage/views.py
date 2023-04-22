from django.shortcuts import render, get_object_or_404
from django.db.models import Min, Max
from services.geocoder import find_closest_storage
from django.conf import settings
import requests
import json

from .models import Storage, Box
from rents.models import Rent


def faq(request):
    return render(request, 'faq.html')


def index(request):

    if settings.DEBUG:

        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        ip_data = json.loads(response.text)
        ip = ip_data['ip']
    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

    response = requests.get('http://ip-api.com/json/' + ip)
    response.raise_for_status()
    address_data = json.loads(response.text)

    client_coordinates = (address_data['lat'], address_data['lon'])

    storages = Storage.objects.all()
    closest_storage = find_closest_storage(client_coordinates, storages)

    total_boxes = closest_storage.boxes.all()
    free_boxes = closest_storage.get_free_boxes()
    lowest_price = total_boxes.order_by('-price')[0].price

    return render(request, 'index.html', {'storage': closest_storage, 'free_boxes': len(free_boxes), 'total_boxes': len(total_boxes), 'lowest_price': lowest_price})


def storages(request):
    storages = Storage.objects.all()
    context = {
        'storages': []
    }

    for storage in storages:
        storage_desc = {
            'specificity': storage.specificity,
            'city': storage.city,
            'street': storage.street,
            'building': storage.building,
            'thumbnail_image': storage.thumbnail_image.url if storage.thumbnail_image else '/static/img/storage_preview.png',
            'slug': storage.slug,
            'avaliable_boxes': storage.get_free_boxes(),
            'boxes_amount': storage.boxes.count,
            'box_min_price': storage.boxes.aggregate(Min('price'))['price__min'],
        }
        context['storages'].append(storage_desc)

    return render(request, 'storages.html', context=context)


def boxes_on_storage(request, slug):
    storages = Storage.objects.all()
    selected_storage = get_object_or_404(Storage, slug=slug)

    context = {
        'storages': []
    }
    context['selected_storage'] = {
            'description': selected_storage.description,
            'specificity': selected_storage.specificity,
            'city': selected_storage.city,
            'street': selected_storage.street,
            'building': selected_storage.building,
            'slug': selected_storage.slug,
            'images': [item.image.url for item in selected_storage.images.all()],
            'avaliable_boxes': {
                'all_boxes': [],
                'to3_area_boxes': [],
                'from3_to10_area_boxes': [],
                'from10_area_boxes': []
            },
            'celsius_temperature': selected_storage.celsius_temperature,
            'boxes_amount': selected_storage.boxes.count,
            'box_min_price': selected_storage.boxes.aggregate(Min('price'))['price__min'],
            'box_max_height': round(selected_storage.boxes.aggregate(Max('height'))['height__max'] / 100, 1)
    }
    avaliable_boxes = selected_storage.get_free_boxes()
    if avaliable_boxes:
        for box in avaliable_boxes:
            box_desc = {
                'number': box.number,
                'price': box.price,
                'width': round(box.width / 100, 1),
                'height': round(box.height / 100, 1),
                'depth': round(box.depth / 100, 1),
                'sq_m_area': round(box.width/100 * box.depth/100, 1)
            }
            context['selected_storage']['avaliable_boxes']['all_boxes'].append(box_desc)
            if box_desc['sq_m_area'] < 3:
                context['selected_storage']['avaliable_boxes']['to3_area_boxes'].append(box_desc)
            elif 3 <= box_desc['sq_m_area'] < 10:
                context['selected_storage']['avaliable_boxes']['from3_to10_area_boxes'].append(box_desc)
            else:
                context['selected_storage']['avaliable_boxes']['from10_area_boxes'].append(box_desc)

    for storage in storages:
        storage_desc = {
            'specificity': storage.specificity,
            'city': storage.city,
            'street': storage.street,
            'building': storage.building,
            'thumbnail_image': storage.thumbnail_image.url if storage.thumbnail_image else '/static/img/storage_preview.png',
            'slug': storage.slug,
            'avaliable_boxes': storage.get_free_boxes(),
            'boxes_amount': storage.boxes.count,
            'box_min_price': storage.boxes.aggregate(Min('price'))['price__min'],
        }
        context['storages'].append(storage_desc)

    return render(request, 'boxes.html', context=context)