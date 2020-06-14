from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404, redirect


def index(request):
    #return HttpResponse("HEllo Python")
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'sign-up.html')


def course(request):
    return render(request, 'courses.html')


def payment(request):
    return render(request, 'payment.html')