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
from django.db.models import Sum, Avg, Q
import io
import datetime
from .forms import TeacherImage, StudentImage


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
            elif user.role == 'admin':
                if user.is_approved == False:
                    return redirect('awating')
                elif  user.is_approved == True & user.is_staff == True:
                    url = reverse('minister', kwargs={'pk': request.user.id})
                    return HttpResponseRedirect(url)
                else:
                    return redirect('awating')
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
        elif user.is_approved == True & user.role == 'parent':
            url = reverse('parent', kwargs={'pk': request.user.id})
            return HttpResponseRedirect(url)
        elif user.is_approved == True & user.role == 'admin' & user.is_staff == True:
            url = reverse('minister', kwargs={'pk': request.user.id})
            return HttpResponseRedirect(url)
    except:
        messages.error(request, 'Account still pending')
        
    return render(request, 'schoolmgt/awating.html')


def adminPage(request, pk):
    user = User.objects.get(id=pk)
    
    if user.is_staff == False:
        return redirect('awating')
    
    else:
        admin, obj = Administration.objects.get_or_create(
            user=user,
        )
    
    students_true = Student.objects.all()
    student_false = User.objects.all().filter(is_approved=False, role='student')
    
    notice = Notice.objects.all()
    
    teacher_true = Teacher.objects.all()
    teacher_false = User.objects.all().filter(is_approved=False, role='teacher')
    
    
    
    context={'students': students_true, 'admins':admin, 'teachers':teacher_true, 'notices':notice}
    return render(request, 'schoolmgt/admin_page.html',  context)

def adminStudent(request):
    
    student_list = Student.objects.all() 
    
    
    
    context = {'student_list':student_list}
    return render(request, 'schoolmgt/admin_student.html', context)


def parrentPage(request, pk):
    
    return render(request, 'schoolmgt/parent_page.html')




def createProfle(request):
    
    return render(request, 'schoolmgt/create_profile.html')

def teacherPage(request, pk):
    user = request.user
    role = user.role
    male_count = 0
    female_count = 0
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    q1 = request.GET.get('q1') if request.GET.get('q1') != None else ''
    q2 = request.GET.get('q2') if request.GET.get('q2') != None else ''
    notice = Notice.objects.all().filter(to=role)
    users = User.objects.get(id=pk)
    
    message = Message.objects.all().filter(recipeient=user)
    teacher, obj = Teacher.objects.get_or_create(
                user = user,
            )
    
    subject = teacher.basic.subject
    basic = teacher.basic
    
    print(f"all subjects: {subject}")
    
    students = Student.objects.all().filter(
            basic=basic
        )
    
    if q1 is '':
        students_list = Student.objects.all().filter(
            basic=basic
        )
    else:
        students_list = Student.objects.filter(
        Q(user__first_name__icontains=q1)|
        Q(user__last_name__icontains=q1)
        )
    
    
    print(f"you queryset is: {q1}")
    print(f"Students are: {students}")
    
    
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
    
    context ={'teacher':teacher, 'user':users, 'basic':basic, 'notices':notice, 'students':students, 
              'student_list':students_list, 'data':data, 'subject': subject, 'q1':q1, 'messagesin':message}
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
    form = TeacherImage(instance=teachers)
    print(user)
    if request.method == "POST":
        date = request.POST.get('date_of_birth')
        format_date = date_converter(date)
        form = TeacherImage(request.POST, request.FILES, instance=teachers)
        
        if form.is_valid():
            form.save()
            
            imj_object = form.instance
            
            context = {'teacher':teachers, 'form':form, 'img_obj': imj_object}
        else:
            form = TeacherImage()
            
        
        
        Teacher.objects.filter(user=user).update(
            address = request.POST.get('address'),
            qualifications = request.POST.get('qualifications'),
            birthday = format_date,
            bio = request.POST.get('bio'),
            
        )
        
        return redirect('teacher-details')
    
    context = {'teacher':teachers, 'form':form}
    return render(request, 'schoolmgt/teacher_form.html', context)



@login_required(login_url='login')
def teacherNotice(request):
    user = request.user
    role = user.role
    notice = Notice.objects.all().filter(to=role)
    
    context = {'notices':notice, 'user':user}
    return render(request, 'schoolmgt/teacher_notice.html', context)
    

def cadetails(request, pk):
    user = request.user
    student = Student.objects.get(id=pk)
    all_ass = Catestexam.objects.filter(student=student)
    teacher = Teacher.objects.get(user=user)
    base = teacher.basic.basic_no
    
    sub = Basic.objects.get(basic_no=base)
    
    subjects = sub.subject.all()
    
    print(f"All subjects: {subjects}")
    
    total = {}
    for subject in subjects:
        ca_exam = Catestexam.objects.filter(student=student, subject=subject).aggregate(Sum("test_score"))
        subs = subject.name
        total[subs] = ca_exam['test_score__sum']
    
    tots = 0
    if None in total.values():
       tots = 0 
    else:
        tots = sum(total.values())
        
        
    Total.objects.update_or_create(
        student=student,
        basic = teacher.basic,
        defaults={'total': tots}
    )
    
    result = Total.objects.get(student=student)
    
    dicts = Total.objects.all().filter(basic=teacher.basic)
    
    print(dicts)
    
    context = {'caexam':all_ass, 'student':student, 'total':total, 'subjects': subjects, 'sum':result}
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
    sub = Basic.objects.get(basic_no=teacher.basic.basic_no)
    subject = sub.subject.all()
    
    print(f"all subs: {subject}")
    
    # subject = []
    
    # for subs in sub:
    #     subject += SubjectB.objects.filter(name=subs)
    
    
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
    
    basic = student.basic
    all_ass = Catestexam.objects.filter(student=student)
    
    
    
    context = {'student':student, 'results':all_ass}
    return render(request, 'schoolmgt/student_page.html', context)


@login_required(login_url='login')
def studentProfileAdd(request):
    user = request.user
    student = Student.objects.get(user=user)
    form = StudentImage(instance=student)
    basic = Basic.objects.all()
    
    if request.method == "POST":
        date = request.POST.get('date_of_birth')
        format_date = date_converter(date)
        form = StudentImage(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
        
        User.objects.filter(id=user.id).update(
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            gender = request.POST.get('gender'),
            phone_number = request.POST.get('phone'),
            email = request.POST.get('email'),
        )
        
        Student.objects.filter(user=user).update(
            birthday= format_date,
            basic = Basic.objects.get(id= request.POST.get('basic')),
            fathers_name = request.POST.get('fathers_name'),
            Mothers_name = request.POST.get('Mothers_name'),
            address = request.POST.get('address'),
            bio = request.POST.get('bio'),
        )
        return redirect('student', pk=user.id)
    context = {'users': user, 'student':student, 'form':form, 'basic':basic}
    return render(request, 'schoolmgt/student_form.html', context)



login_required(login_url='login')
def studentResult(request, pk):
    user = request.user
    student = Student.objects.get(id=pk)
    basic = student.basic
    all_ass = Catestexam.objects.filter(student=student)
    teacher = Teacher.objects.get(basic=basic)
    base = teacher.basic.basic_no
    
    sub = Basic.objects.get(basic_no=base)
    
    subjects = sub.subject.all()
    
    total = {}
    
    for subject in subjects:
        ca_exam = Catestexam.objects.filter(student=student, subject=subject).aggregate(Sum("test_score"))
        subs = subject.name
        total[subs] = ca_exam['test_score__sum']
    
    context = {'caexam':all_ass, 'student':student, 'total':total, 'subjects': subjects}
    
    return render(request, 'schoolmgt/result_fee.html', context)




    
        
        
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
    