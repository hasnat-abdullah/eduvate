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
from django.urls import path
from eduvate import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.getIndex, name='index'),
    path('login', views.getLogin, name='login'),
    path('signup', views.getSignup, name='signup'),
    path('logout', views.getLogout, name='logout'),
    path('dashboard', views.getDashboard, name='dashboard'),
    path('course', views.getCourse, name='course'),
    path('running-course', views.getRunningCourse, name='runningCourse'),
    path('course/<int:id>/', views.getSingleCourse, name='singleCourse'),
    path('scales/', views.getScaleList, name='scaleList'),
    path('scale/<int:scaleId>/', views.getScale, name='scale'),
    path('save_score/<int:scaleId>/', views.getSaveScore, name='saveScore'),
    path('payment', views.getPayment, name='payment'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)