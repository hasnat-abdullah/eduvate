from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404, redirect
from django.views import View


def payment(request):
    return render(request, 'payment.html')


class Courses(View):
    def get(self,request):
        return render(request, 'lms/student-courses.html')
