from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid
from django.utils.translation import gettext_lazy as _
import random
from django.db.models import Model
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

ACESSMENT = (
    ("1st C.A", "1st C.A"),
    ("2nd C.A", "2nd C.A"),
    ("Exams", "Exams"),
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
        return f"{self.first_name} {self.last_name} : {self.role}, is_approved: {self.is_approved}"
    
class SubjectB(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name

class Basic(models.Model):
    basic_no = models.CharField(max_length=50)
    
    
    def __str__(self) -> str:
        return self.basic_no
    

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    basic = models.ForeignKey(Basic, on_delete=models.SET_NULL, blank=True, null=True )
    birthday = models.DateField()
    address= models.CharField(max_length=120, blank=True, null=True)
    fathers_name = models.CharField(max_length=50, default='john')
    Mothers_name = models.CharField(max_length=50, default='janet')
    status = models.BooleanField()
    image = models.ImageField(null=True, default="testimon.png")
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
    
    
    def get_gender(self):
        genders = self.user_set.all()
        
        return genders

    
class Charts(models.Model):
        basic = basic = models.ForeignKey(Basic, on_delete=models.SET_NULL, blank=True, null=True )
        image = models.ImageField(null=True, default="testimon.png")
    
    
    
class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #midle_name = models.CharField(max_length=100, blank=True)
    basic = models.OneToOneField(Basic, on_delete=models.SET_NULL, blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    subject = models.ManyToManyField(SubjectB, related_name='Subject', blank=True)
    address = models.CharField(max_length=100,  blank=True, null=True)
    qualifications = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=400, blank=True)
    image = models.ImageField(null=True, default="testimon.png")
    unique_id = models.CharField(default=uuid.uuid4().hex[:5].upper(), max_length=10, editable=False)
    
    
    def __str__(self) -> str:
        return self.user.first_name
    

    
class Fees(models.Model):
    basic = models.ForeignKey(Basic, on_delete=models.SET_NULL, blank=True, null=True)
    Fee = models.IntegerField() 
    

class Attendance(models.Model):
    basic = models.ForeignKey(Basic, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)


class Catestexam(models.Model):
    test_type = models.CharField(max_length=50, choices=ACESSMENT)
    subject = models.ForeignKey(SubjectB, related_name='subject', on_delete=models.CASCADE, blank=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    test_score = models.IntegerField(blank=False)
    
    
    def __str__(self) -> str:
        return f"{self.test_type} for {self.student.user.first_name} in {self.subject}"

class Total(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    subject = models.ForeignKey(SubjectB, on_delete=models.CASCADE, blank=False)
    total = models.IntegerField(blank=False)
    
   
    
class Results(models.Model):
    Student=models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    result_score = models.IntegerField(blank=False, null=False)
   
    
