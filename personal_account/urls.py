from django.urls import path, include
from .views import my_rent_view

urlpatterns = [
    path('', my_rent_view, name='my-rent')
]
