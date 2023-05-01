from django.shortcuts import render, redirect
from django.contrib import messages
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
    
    return render(request, 'schoolmgt/awating.html')
    

def createProfle(request):
    
    return render(request, 'schoolmgt/create_profile.html')

def teacherPage(request, pk):
    user = User.objects.get(id=pk)
    user_name = request.user.first_name
    if not Teacher.objects.filter(user=user).exists():
        return redirect('profile')
    else:
        teacher = Teacher.objects.get(user=user)
        print(user)
        print(teacher)
    
    context ={'teacher':teacher, 'user':user}
    return render(request, 'schoolmgt/teacherpage.html', context)


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