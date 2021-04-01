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
from django.urls import path, include
from eduvateApp import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.LoginView.as_view(), name='login'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),

    path('enroll_course/<int:id>/', views.EnrollCourseView.as_view(), name='enrollCourse'),
    path('running-course', views.RunningCourseView.as_view(), name='runningCourse'),
    path('course/', include([
        path('', views.CourseListView.as_view(), name='course'),
        path('<int:id>/', views.CourseDetailsView.as_view(), name='singleCourse'),
        path('<int:cid>/<int:sid>', views.CourseSessionView.as_view(), name='CourseSession'),
        path('<int:cid>/<int:sid>/<int:lid>', views.TakeCourseView.as_view(), name='takeCourse'),
    ])),

    path('permission_denied/', views.getDenied, name='denied'),

    path('scales/', views.ScaleListView.as_view(), name='scaleList'),
    path('scale/<int:scaleId>/', views.ScaleDetailsView.as_view(), name='scale'),
    path('save_score/<int:scaleId>/', views.SaveScoreView.as_view(), name='saveScore'),
    path('test_result/', views.TestResultView.as_view(), name='testResult'),

    path('save_user_input/<int:lessonId>/', views.SaveLessonFeedbackView.as_view(), name='saveUserInput'),

    path('payment', views.getPayment, name='payment')
]
