from datetime import timedelta

import qrcode
from django.db.models import F, ExpressionWrapper, BooleanField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from rents.models import Rent
from storage.models import Box
from .forms import RegisterUserForm, LoginUserForm, ProfileForm
from .models import Client
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


@login_required
def my_rent_view(request):
    client = Client.objects.get(email=request.user.email)
    rents = Rent.objects.filter_active(client)

    initial_data = {
        'email': client.email,
        'phone_number': client.phone_number,
    }

    profile_form = ProfileForm(initial=initial_data)
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.error(request, 'Пароли не сходятся!')
            return render(request, 'my-rent.html', {'profile_form': profile_form})

        elif len(password1) < 8:
            messages.error(request, 'Пароль должен быть не меньше восьми символов!')
            return render(request, 'my-rent.html', {'profile_form': profile_form})

        elif Client.objects.filter(email=request.POST['email']).exclude(id=client.id):
            messages.error(request, 'Такая почта уже используется!')
            return render(request, 'my-rent.html', {'profile_form': profile_form})

        else:
            if client.email != request.POST['email']:
                client.email = request.POST['email']
            client.phone_number = request.POST['phone_number']
            client.set_password(password1)
            client.save()

            logout(request)
            client = authenticate(email=client.email, password=password1)
            login(request, client)

            initial_data = {
                'email': client.email,
                'phone_number': client.phone_number,
            }
            profile_form = ProfileForm(initial=initial_data)

            return render(request, 'my-rent.html', {'profile_form': profile_form})

    return render(request, 'my-rent.html', {'profile_form': profile_form, 'rents': rents})


def inject_register_form(request):
    return {'register_form': RegisterUserForm()}


def inject_login_form(request):
    return {'login_form': LoginUserForm()}


def login_view(request):
    if request.method == 'POST':

        if 'login_form' in request.POST:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('my-rent')
            else:
                messages.error(request, 'Что-то пошло не так(')
                return redirect('index')

        elif 'register_form' in request.POST:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('my-rent')
            else:
                messages.error(request, 'Что-то пошло не так(')
                return redirect('index')

    return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('index')


def send_qr(request, box_id):
    box = Box.objects.filter(id=box_id).select_related('storage').first()
    img = qrcode.make(f'box #{box.id} in {box.storage.slug}')
    img.save('qr.png')
    return my_rent_view(request)
