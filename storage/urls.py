from django.urls import path

from storage.views import show_my_orders

urlpatterns = [
    path('active/', show_my_orders)
]
