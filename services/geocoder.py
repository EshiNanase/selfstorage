from geopy import distance
from django.conf import settings
import requests


def find_closest_storage(client_coordinates, storages):
    closest_storage = {
        'storage': storages[0],
        'distance': distance.distance((storages[0].latitude, storages[0].longitude), client_coordinates)
    }
    for storage in storages[1:]:
        storage_coordinates = (storage.latitude, storage.longitude)
        distance_between_client_and_storage = distance.distance(storage_coordinates, client_coordinates)
        if distance_between_client_and_storage < closest_storage['distance']:
            closest_storage['storage'] = storage
            closest_storage['distance'] = distance_between_client_and_storage

    return closest_storage['storage']


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def set_coordinates(storage):
    address = f'город {storage.city}, улица {storage.street}, дом {storage.building}'
    try:
        coordinates = fetch_coordinates(settings.YANDEX_API_TOKEN, address)[::-1]
    except TypeError:
        coordinates = (None, None)
    return coordinates
