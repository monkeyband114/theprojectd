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
from django.db.models import Sum, Avg
import io
import datetime
from .forms import UserImage


def errorPage(request):
    
    return render(request, 'schoolmgt/404.html')


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
            return redirect('login')
        else:
            messages.error(request, 'An error has occored')
    
    return render(request, 'schoolmgt/register.html',  {'form':form})


    
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
    male_count = 0
    female_count = 0
    users = User.objects.get(id=pk)
    
    teacher, obj = Teacher.objects.get_or_create(
                user = user,
            )
    subject = teacher.subject.all()
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
    
    context ={'teacher':teacher, 'user':users, 'basic':basic, 'students':students, 'data':data, 'subject': subject}
    return render(request, 'schoolmgt/teacherpage.html', context)




def teacherDetails(request):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    
    
    context={'teacher':teacher}
    return render(request, 'schoolmgt/teacher_details.html', context)


@login_required(login_url='login')
def teacherProfleAdd(request):
    user = request.user
    teachers = Teacher.objects.get(user=user)
    form = UserImage(instance=teachers)
    print(user)
    if request.method == "POST":
        date = request.POST.get('date_of_birth')
        format_date = date_converter(date)
        form = UserImage(request.POST, request.FILES, instance=teachers)
        
        if form.is_valid():
            form.save()
            
            imj_object = form.instance
            
            context = {'teacher':teachers, 'form':form, 'img_obj': imj_object}
        else:
            form = UserImage()
            
        
        
        Teacher.objects.filter(user=user).update(
            address = request.POST.get('address'),
            qualifications = request.POST.get('qualifications'),
            birthday = format_date,
            bio = request.POST.get('bio'),
            
        )
        
        return redirect('teacher-details')
    
    context = {'teacher':teachers, 'form':form}
    return render(request, 'schoolmgt/teacher_form.html', context)



def cadetails(request, pk):
    user = request.user
    student = Student.objects.get(id=pk)
    all_ass = Catestexam.objects.filter(student=student)
    teacher = Teacher.objects.get(user=user)
    subjects = teacher.subject.all()
    
    total = {}
    
    for subject in subjects:
        ca_exam = Catestexam.objects.filter(student=student, subject=subject).aggregate(Sum("test_score"))
        print(ca_exam)
        subs = subject.name
        total[subs] = ca_exam['test_score__sum']
    
    
    
    print(total)
    
    context = {'caexam':all_ass, 'student':student, 'total':total, 'subjects': subjects}
    return render(request, 'schoolmgt/ca_page.html', context)


def calculate_results(request, pk):
    
    student = Student.objects.get(id=pk)
    all_ass = Catestexam.objects.filter(student=student)
    subjects = student.subjects.name
    
    total = 0
    
    for ass in all_ass:
        for subject in subjects:
            ca_exam = Catestexam.objects.filter(student=student, subject=subject)
            total = ca_exam.aggregate(sum('test_score'))
    
    
def caadd(request, pk):
    student = Student.objects.get(id=pk)
    stud = student.basic
    teacher = Teacher.objects.get(basic=stud)
    print(teacher)
    sub = teacher.subject.all()
    print(sub)
    
    subject = []
    
    for subs in sub:
        subject += SubjectB.objects.filter(name=subs)
    
    
    if request.method == 'POST':
        obj, created = Catestexam.objects.update_or_create(
            test_type = request.POST.get('test_type'),
            subject = SubjectB.objects.get(id=request.POST.get('subject')),
            student = student,
            defaults = {'test_score': request.POST.get('test_score')}
        )
        
        return redirect('capage', pk=student.id)
    context = {'student':student, 'subjects':subject}
    return render(request, 'schoolmgt/addca.html', context)




@login_required(login_url='login')
def studentPage(request, pk):
    user = request.user
    student, obj = Student.objects.get_or_create(
        user = user
        
    )
    
    
    context = {'student':student}
    return render(request, 'schoolmgt/student_page.html', context)








    
        
        
def date_converter(date_str):
  # Parse the date string into a datetime object.
  try:
    datetime_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
  except ValueError:
    try:
      datetime_obj = datetime.datetime.strptime(date_str, "%B %d, %Y")
    except ValueError:
      raise ValueError("Invalid date string: {}".format(date_str))

  # Convert the datetime object to a string in yyyy-mm-dd format.
  return datetime_obj.strftime("%Y-%m-%d")
    