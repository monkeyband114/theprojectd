from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.registerUser, name='register'),
    path('login-page/', views.loginpage, name='login'),
    path('awating/', views.awaitingPage, name='awating'),
    path('studentpage/', views.studentPage, name='student'),
    path('teacherpage/', views.teacherPage, name='teacher'),
]