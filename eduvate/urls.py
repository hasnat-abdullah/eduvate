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
from django.contrib import admin
from django.conf.urls import url,include
from eduvate import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.getIndex, name='index'),
    url(r'^login', views.getLogin, name='login'),
    url(r'^signup', views.getSignup, name='signup'),
    url(r'^course', views.getCourse, name='course'),
    url(r'^payment', views.getPayment, name='payment'),
    url(r'^student/', include('studentApp.urls')),
    url(r'^course/', include('courseApp.urls')),
    url(r'^appointment/', include('appointmentApp.urls')),
    url(r'^exam/', include('examApp.urls')),
    url(r'^instructor/', include('instructorApp.urls')),
    url(r'^payment/', include('paymentApp.urls')),
    url(r'^blog/', include('blogApp.urls')),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)