from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MyUserStartForm
from django.views.decorators.csrf import csrf_protect 
from django.contrib.auth import authenticate, login, logout
from . models import User, Student, Teacher
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    user = User.objects.get(id=pk)
    teacher = Teacher.objects.get(user=user)
    basic = teacher.basic
    students = Student.objects.all().filter(basic=basic)
    
    if not Teacher.objects.filter(user=user).exists():
        return redirect('profile')
    else:
        teacher = Teacher.objects.get(user=user)
    
    
    context ={'teacher':teacher, 'user':user, 'basic':basic, 'students':students}
    return render(request, 'schoolmgt/teacherpage.html', context)


def teacherDetails(request):
    
    context={}
    return render(request, 'schoolmgt/teacher_details.html', context)


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
    print(user)
    if request.method == "POST":
        Teacher.objects.create(
            user = user,
            address = request.POST.get('address'),
            qualifications = request.POST.get('qualifications'),
            birthday = request.POST.get('date_of_birth'),
            bio = request.POST.get('bio'),
        )
        
        url = reverse('teacher', kwargs={'pk': request.user.id})
        return HttpResponseRedirect(url)
    
    context = {}
    return render(request, 'schoolmgt/teacher_form.html', context)



    
        
        
    