from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404, redirect


def index(request):
    #return HttpResponse("HEllo Python")
    return render(request,'lms/index.html')