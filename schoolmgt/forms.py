from django.forms import ModelForm, fields 
from . models import User, Teacher, Student
from django.contrib.auth.forms import UserCreationForm
from django.db import models 
from django import forms  

class MyUserStartForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'gender', 'email', 'phone_number', 'role', 'password1', 'password2']
  
  
class TeacherImage(ModelForm):  
    class Meta:  
        model = Teacher
        fields = ['image']


class StudentImage(ModelForm):
    class Meta:
        model = Student
        fields = ['image']