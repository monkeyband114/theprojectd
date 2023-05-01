from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.registerUser, name='register'),
    path('login-page/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name="logout"),
    path('awating/', views.awaitingPage, name='awating'),
    path('createpro/', views.createProfle, name='profile'),
    path('studentpage/<str:pk>/', views.studentPage, name='student'),
    path('teacherpage/<str:pk>/', views.teacherPage, name='teacher'),
]