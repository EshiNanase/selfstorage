from django.shortcuts import render


def faq(request):
    return render(request, 'faq.html')


def index(request):
    return render(request, 'index.html')
