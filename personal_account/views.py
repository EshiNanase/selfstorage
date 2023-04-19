from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import RegisterUserForm, LoginUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def my_rent_view(request):
    if request.method == 'POST':

        if 'login_form' in request.POST:
            form = LoginUserForm(request.POST)
            data = form.cleaned_data
            email = data['email']
            password = data['password']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('my-rent')

        elif 'register_form' in request.POST:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('my-rent')

    return render(request, 'my-rent.html')


def inject_register_form(request):
    return {'register_form': RegisterUserForm()}


def inject_login_form(request):
    return {'login_form': LoginUserForm()}
