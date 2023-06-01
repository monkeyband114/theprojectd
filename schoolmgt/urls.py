from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('404Erorr/', views.errorPage, name='Error'),
    path('signup/', views.registerUser, name='register'),
    path('login-page/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('awating/', views.awaitingPage, name='awating'),
    path('createpro/', views.createProfle, name='profile'),
    path('teaher-details/', views.teacherDetails, name='teacher-details'),
    path('ca-add/<str:pk>', views.caadd, name='caadd'),
    path('create-teacher/', views.teacherProfleAdd, name="teacher-add"),
    path('teacherpage/<str:pk>/', views.teacherPage, name='teacher'),
    path('capage/<str:pk>/', views.cadetails, name='capage'),
    path('studentpage/<str:pk>/', views.studentPage, name='student'),
    path('update-student/', views.studentProfileAdd, name='student-add'),
    path('Result&fees/<str:pk>/', views.studentResult, name='results'),
    path('notice-page/', views.teacherNotice, name='teacher-notice'),
    path('admin-page/<str:pk>/', views.adminPage, name="minister"), 
    path('all-students/', views.adminStudent, name='admin-student'),
    path('parrent-page/', views.parrentPage, name='parent'),
    
] 