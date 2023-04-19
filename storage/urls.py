from django.urls import path

from storage.views import faq, index, boxes

urlpatterns = [
    path('faq/', faq, name='faq'),
    path('', index, name='index'),
    path('boxes/', boxes, name='boxes'),
]