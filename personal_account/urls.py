from django.urls import path, include
from .views import my_rent_view, logout_view, login_view
from django.urls import path

urlpatterns = [
    path('', my_rent_view, name='my-rent'),
    path('logout', logout_view, name='logout'),
    path('login', login_view, name='login')
]
