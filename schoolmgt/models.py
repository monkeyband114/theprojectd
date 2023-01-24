from django.db import models
from django.contrib.auth.models import User


class SubjectB(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.name

class Basic(models.Model):
    basic_no = models.CharField(max_length=50)
    subjects = models.ManyToManyField(SubjectB, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.basic_no
    
gen_chices = (
    ("male", "male"),
    ("female", "female")
)

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    midle_name = models.CharField(max_length=100)
    basic = models.OneToOneField(Basic, on_delete=models.SET_NULL, blank=True, null=True )
    gender = models.CharField(max_length=50, choices=gen_chices)
    parentS_name = models.CharField(max_length=50, default='john')
    
    def __str__(self) -> str:
        return self.first_name
    
class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    midle_name = models.CharField(max_length=100)
    basic = models.OneToOneField(Basic, on_delete=models.SET_NULL, blank=True, null=True )
    gender = models.CharField(max_length=50, choices=gen_chices)
    phone = models.CharField(max_length=16)
    
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
