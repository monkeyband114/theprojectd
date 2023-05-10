from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MyUserStartForm
from django.views.decorators.csrf import csrf_protect 
from django.contrib.auth import authenticate, login, logout
from . models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
import matplotlib.pyplot as plt
import io
import base64
import urllib, base64
import os



def generate_pie_chart(data, basic):
    labels = ['Male', 'Female']
    sizes = [data['male'], data['female']]
    colors = ['lightblue', 'pink']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Male vs. Female Students')
    plt.legend(title='Gender', loc='best')
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_data = buffer.getvalue()
    buffer.close()





def home(request):
    context = {}
    
    return render(request, 'schoolmgt/index.html')


    
def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Account not found')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.role == 'teacher':
                if user.is_approved == False:
                    return redirect('awating')
                else:
                    url = reverse('teacher', kwargs={'pk': request.user.id})
                    return HttpResponseRedirect(url)
            elif user.role == 'student':
                if user.is_approved == False:
                    return redirect('awating')
                else:
                    url = reverse('student', kwargs={'pk': request.user.id})
                    return HttpResponseRedirect(url)
            else:
                return redirect('home')
        else:
            messages.error(request, 'omo password not found')
            
    # remember to upgrade the above if statement when the you add admin page 
    context= {}
    return render(request, 'schoolmgt/login_hm.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home') 



def awaitingPage(request):
    user = request.user 
    try: 
        if user.is_approved == True & user.role == 'teacher':
            url = reverse('teacher', kwargs={'pk': request.user.id})
            return HttpResponseRedirect(url)
        
        elif user.is_approved == True & user.role == 'student':
             url = reverse('student', kwargs={'pk': request.user.id})
             return HttpResponseRedirect(url)
    except:
        messages.error(request, 'Account still pending')

        
    return render(request, 'schoolmgt/awating.html')
    

def createProfle(request):
    
    return render(request, 'schoolmgt/create_profile.html')

def teacherPage(request, pk):
    user = request.user
    genders = user.gender
    male_count = 0
    female_count = 0
    users = User.objects.get(id=pk)
    teacher = Teacher.objects.get(user=user)
    basic = teacher.basic
    students = Student.objects.all().filter(basic=basic)
    
    if not Teacher.objects.filter(user=user).exists():
        return redirect('profile')
    else:
        teacher = Teacher.objects.get(user=user)
    
    for student in students: 
         if student.user.gender == 'male':
             male_count = male_count + 1
         else:
              female_count = female_count + 1

            
    
    print(male_count)
    data = {
        'male': male_count,
        'female': female_count
    }
    
    context ={'teacher':teacher, 'user':users, 'basic':basic, 'students':students, 'data':data}
    return render(request, 'schoolmgt/teacherpage.html', context)


def teacherDetails(request):
    
    context={}
    return render(request, 'schoolmgt/teacher_details.html', context)


def cadetails(request, pk):
    student = Student.objects.get(id=pk)
    
    
    ca_exam = Catestexam.objects.all().filter(student=student)
    
    context = {'caexam':ca_exam, 'student':student}
    return render(request, 'schoolmgt/ca_page.html', context)




def caadd(request, pk):
    student = Student.objects.get(id=pk)
    stud = student.basic
    teacher = Teacher.objects.get(basic=stud)
    print(teacher)
    subject = teacher.subject.all()
    
    print(subject)
    if request.method == 'POST':
        Catestexam.objects.create(
            test_type = request.POST.get('test_type'),
            subject = request.POST.get('subject'),
            student = student,
            test_score = request.POST.get('test_score'),
        )
        
    context = {'student':student, 'subjects':subject}
    return render(request, 'schoolmgt/addca.html', context)





def studentPage(request, pk):
    
    context ={}
    return render(request, 'schoolmgt/student_page.html', context)



@csrf_protect
def registerUser(request):
    
    form = MyUserStartForm()
    
    if request.method == 'POST':
        form = MyUserStartForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.first_name = user.first_name.lower()
            # user.last_name = user.last_name.lower()
            user.save()
            print('done')
            # login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'An error has occored')
    
    return render(request, 'schoolmgt/register.html',  {'form':form})


@login_required(login_url='login')
def teacherProfleAdd(request):
    user = request.user
    teachers = Teacher.objects.get(user=user)
    print(user)
    if request.method == "POST":
        Teacher.objects.update(
            user = user,
            address = request.POST.get('address'),
            qualifications = request.POST.get('qualifications'),
            birthday = request.POST.get('date_of_birth'),
            bio = request.POST.get('bio'),
        )
        
        url = reverse('teacher', kwargs={'pk': request.user.id})
        return HttpResponseRedirect(url)
    
    context = {'teacher':teachers}
    return render(request, 'schoolmgt/teacher_form.html', context)



    
        
        
    