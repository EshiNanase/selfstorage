from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterUserForm, LoginUserForm, ProfileForm
from .models import Client
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


@login_required
def my_rent_view(request):

    client = Client.objects.get(email=request.user.email)

    initial_data = {
        'email': client.email,
        'phone_number': client.phone_number,
        'password': client.password
    }
    profile_form = ProfileForm(initial=initial_data)

    if request.method == 'POST':

        if 'profile_form' in request.POST:
            pass

    return render(request, 'my-rent.html', {'profile_form': profile_form})


def inject_register_form(request):
    return {'register_form': RegisterUserForm()}


def inject_login_form(request):
    return {'login_form': LoginUserForm()}


def login_view(request):

    if request.method == 'POST':

        if 'login_form' in request.POST:
            form = LoginUserForm(request.POST)
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('my-rent')
            else:
                messages.error(request, 'Что-то пошло не так(')
                return redirect('my-rent')

        elif 'register_form' in request.POST:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('my-rent')
            else:
                messages.error(request, 'Что-то пошло не так(')
                return redirect('my-rent')

        elif 'profile_form' in request.POST:
            pass

    return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('index')
