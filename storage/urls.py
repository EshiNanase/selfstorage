from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from storage.views import faq, index, boxes_on_storage, storages

urlpatterns = [
    path('faq/', faq, name='faq'),
    path('', index, name='index'),
    path('storages/', storages, name='storages'),
    path('boxes/<slug>', boxes_on_storage, name='boxes_on_storage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)