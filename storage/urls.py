from django.urls import path

from storage.views import faq, index

urlpatterns = [
    path('faq/', faq, name='faq'),
    path('', index, name='index'),
]