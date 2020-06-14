"""eduvate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from studentApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^dashboard', views.dashboard, name='payment'),
    url(r'^courses', views.Courses.as_view(), name='courses'),
    # url(r'^Profile', views.payment, name='payment'),
    # url(r'^billing', views.payment, name='payment'),
    # url(r'^payment', views.payment, name='payment'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)