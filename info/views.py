from django.contrib import messages  # ✅ Correct
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from .models import Marks
from .models import studentinfo as student, studentinfo
from django.core.files.storage import FileSystemStorage
# Create your views here.
def shome(request):
    return render(request, 'home.html')
def registration(req):
    if req.method=='POST':
        rollno=req.POST.get('roll no')
        stname=req.POST.get('stname')
        password=req.POST.get('password')
        cnfpassword=req.POST.get('conf pass')
        phone=req.POST.get('phone')
        email=req.POST.get('email')
        photo=req.FILES.get('photo')
        c=0
        s=0
        u=0
        l=0
        d=0
        for i in password:
            c+=1
            if i.isupper():
                u+=1
            elif i.islower():
                l+=1
            elif i.isdigit():
                d+=0
            else:
                s+=1
        if c>=8 or c<=16 and u>=1 and l>=1 and s>=1 and d>=1:
            r='valid'
        else:
            r='Invalid Password'
            return render(req,'registration.html',{'r':r})
        if password != cnfpassword:
            return render(req,'registration.html',{'r':'Password and Conform Password should match'})
        if not phone.isdigit() or len(phone)!=10:
            return render(req,'registration.html',{'r':'Invalid Phone Number'})
        if not email.endswith('@gmail.com'):
            return render(req,'registration.html',{'r':'Invalid Email'})
        info=student(rollno=rollno,name=stname,password=password,confpass=cnfpassword,phoneno=phone,email=email,image=photo)
        info.save()
        return render(req,'success.html',{'student':info})
    return render(req,'registration.html')
def lon(request):
    if request.method == 'POST':
        rollno = request.POST.get('roll no')
        password = request.POST.get('password')

        try:
            student = studentinfo.objects.get(rollno=rollno)
            if student.password == password:
                # Login success: set session and redirect
                request.session['rollno'] = student.rollno
                request.session['student_name'] = student.name
                return render(request, 'student.html', {
                    'student': student,
                    'name': student.name
                })
            else:
                return render(request, 'login.html', {'r': 'Invalid password'})
        except studentinfo.DoesNotExist:
            return render(request, 'login.html', {'r': 'Roll number not registered'})
    else:
        return render(request, 'login.html')
def success(req):
    return render(req,'success.html')
def logout_view(req):
    req.session.flush()
    return redirect('login')
from django.shortcuts import render, redirect
from .models import studentinfo

def sdetails(request):
    rollno = request.session.get('rollno')
    if not rollno:
        return redirect('login')  # Not logged in

    try:
        student = studentinfo.objects.get(rollno=rollno)
    except studentinfo.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        student.name = request.POST.get('stname')
        student.email = request.POST.get('email')
        student.phoneno = request.POST.get('phone')

        if request.FILES.get('photo'):
            student.image = request.FILES['photo']

        student.save()
        return render(request, 'details.html', {
            'student': student,
            'msg': '✅ Details updated successfully!'
        })

    return render(request, 'details.html', {'student': student})
def ssearch(request):
    student = None
    error = ''

    if request.method == 'POST':
        rollno = request.POST.get('rollno')
        try:
            student = studentinfo.objects.get(rollno=rollno)
        except studentinfo.DoesNotExist:
            error = "❌ Student with Roll No {} not found.".format(rollno)

    return render(request, 'search.html', {'student': student, 'error': error})
def add_marks(request):
    if request.method == 'POST':
        rollno = request.POST.get('rollno')
        try:
            student = studentinfo.objects.get(rollno=rollno)
            english = int(request.POST.get('english'))
            hindi = int(request.POST.get('hindi'))
            telugu = int(request.POST.get('telugu'))
            maths = int(request.POST.get('maths'))
            science = int(request.POST.get('science'))
            social = int(request.POST.get('social'))

            # If already exists, update
            mark, created = Marks.objects.update_or_create(
                student=student,
                defaults={
                    'english': english,
                    'hindi': hindi,
                    'telugu': telugu,
                    'maths': maths,
                    'science': science,
                    'social': social
                }
            )
            return render(request, 'amarks.html', {'message': 'Marks submitted successfully ✅'})
        except studentinfo.DoesNotExist:
            return render(request, 'amarks.html', {'message': 'Student not found ❌'})

    return render(request, 'amarks.html')
def marks_view(request):
    rollno = request.session.get('rollno')
    if rollno:
        try:
            student = studentinfo.objects.get(rollno=rollno)
            marks = Marks.objects.get(student=student)
            return render(request, 'marks.html', {'marks': marks})
        except:
            return render(request, 'marks.html', {'marks': None})
    else:
        return redirect('login')
    return redirect('login')
def sstudent(req):
    return render(req,'student.html')
def Adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'sunil' and password == 'Sunil@0975':
            request.session['is_admin'] = True
            return redirect('admin')
        else:
            return render(request, 'Adminlogin.html', {'error': 'Invalid admin credentials'})

    return render(request, 'Adminlogin.html')
def admin1(request):
    student_count = studentinfo.objects.count()
    return render(request, 'admin.html', {'student_count': student_count})
def admin_students(request):
    students = studentinfo.objects.all()
    return render(request, 'aupdate.html', {'students': students})

def admin_update_delete(request, rollno):
    student = get_object_or_404(studentinfo, rollno=rollno)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update':
            student.name = request.POST.get('name')
            student.phoneno = request.POST.get('phoneno')
            student.email = request.POST.get('email')
            student.password = request.POST.get('password')
            student.confpass = request.POST.get('confpass')
            if request.FILES.get('image'):
                student.image = request.FILES.get('image')
            student.save()
            messages.success(request, f"✅ Student {student.name}'s record updated.")
        elif action == 'delete':
            student.delete()
            messages.success(request, f"🗑️ Student with Roll No {rollno} deleted.")
        return redirect('admin_students')
def admin_marks_view(request):
    all_marks = Marks.objects.select_related('student').all()
    return render(request, 'admin_marks.html', {'all_marks': all_marks})





