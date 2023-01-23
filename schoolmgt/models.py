from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    midle_name = models.CharField(max_length=100)
    basic = models.CharField(max_length=200)
    gender = models.CharField(max_length=50)

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    midle_name = models.CharField(max_length=100)
    basic = models.CharField(max_length=200)
    gender = models.CharField(max_length=50)
    
class Basic(models.Model):
    basic_no = models.CharField(max_length=50)
    no_students = models.IntegerField(max_length=100)
    
    
    def __str__(self) -> str:
        return self.basic_no
    
    
class Fees(models.Model):
    basic = models.ForeignKey(Basic, on_delete=models.SET_NULL, blank=True, null=True)
    Fee = models.IntegerField(max_length=100)
    

class Attendance(models.Model):
    basic = models.ForeignKey(Basic, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateField(auto_now_add=True)