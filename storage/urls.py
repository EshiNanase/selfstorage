from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from storage.views import faq, index, boxes

urlpatterns = [
    path('faq/', faq, name='faq'),
    path('', index, name='index'),
    path('boxes/', boxes, name='boxes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)