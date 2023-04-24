from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

gen_chices = (
    ("male", "male"),
    ("female", "female")
)

ROLE_CHOICES = (
    ("teacher", "teacher"),
    ("student", "student"),
)


class User(AbstractBaseUser, PermissionsMixin):
    first_name=models.CharField(max_length=200, null=True)
    last_name =models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=50, choices=gen_chices)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(null=True, max_length=16)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    is_approved=models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    # avatar
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    
    
class SubjectB(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name

class Basic(models.Model):
    basic_no = models.CharField(max_length=50)
    subjects = models.ManyToManyField(SubjectB, blank=True)
    
    def __str__(self) -> str:
        return self.basic_no
    


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    midle_name = models.CharField(max_length=100)
    basic = models.OneToOneField(Basic, on_delete=models.SET_NULL, blank=True, null=True )
    birthday = models.DateField()
    gender = models.CharField(max_length=50, choices=gen_chices)
    fathers_name = models.CharField(max_length=50, default='john')
    Mothers_name = models.CharField(max_length=50, default='janet')
    status = models.BooleanField()
    
    
    def __str__(self) -> str:
        return self.first_name
    
class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    midle_name = models.CharField(max_length=100, blank=True)
    basic = models.OneToOneField(Basic, on_delete=models.SET_NULL, blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    # date_birth
    def __str__(self) -> str:
        return self.first_name

    

    
class Fees(models.Model):
    basic = models.ForeignKey(Basic, on_delete=models.SET_NULL, blank=True, null=True)
    Fee = models.IntegerField()
    

class Attendance(models.Model):
    basic = models.ForeignKey(Basic, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
