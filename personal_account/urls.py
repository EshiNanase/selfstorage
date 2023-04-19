from django.urls import path, include
from .views import my_rent_view
from django.urls import path

urlpatterns = [
    path('', my_rent_view, name='my-rent')
]
