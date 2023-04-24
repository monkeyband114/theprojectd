from django.forms import ModelForm
from . models import User
from django.contrib.auth.forms import UserCreationForm

class MyUserStartForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'gender', 'email', 'phone_number', 'role', 'password1', 'password2']
        




