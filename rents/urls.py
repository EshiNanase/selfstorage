from django.urls import path

from .views import show_my_rents

urlpatterns = [
    path('active/', show_my_rents)
]
