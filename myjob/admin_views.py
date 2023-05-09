from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound


def index(request):
    if request.user.is_anonymous or not request.user.is_superuser:
        return redirect('/admin/login/?next=/admin/')
    return render(request, 'pages/dashboard.html')


def billing(request):
    return HttpResponseNotFound()


def profile(request):
    return HttpResponseNotFound()


def tables(request):
    return HttpResponseNotFound()


def rtl(request):
    return HttpResponseNotFound()


def vr(request):
    return HttpResponseNotFound()
