from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Lecture
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            new_rating = float(request.POST.get('rating', 0))
            if course.count == 0:
                course.rate = new_rating
            else:
                course.rate = (course.rate * course.count + new_rating) / (course.count + 1)
            course.count += 1
            course.save()
            return redirect('courses:course_detail', id=course.id)
    
        return render(request, 'course_detail.html', {'course': course})
    else:
        return HttpResponseRedirect("/courses/login")


def register(request):
    if request.method == "GET":
        return render(request, "register.html", {})
    firstname = request.POST['fname']
    lastname = request.POST['lname']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    age = request.POST['age']

    user = User.objects.create_user(first_name = firstname,
                                    last_name = lastname,
                                    username = username,
                                    password = password,
                                    email = email)
    user.save()
    lec = Lecture(user = user, age = age)
    lec.save()
    return HttpResponseRedirect("/courses/login")

def login(request):
    if request.method == "GET":
        return render(request, "login.html", {})
    
    usr = request.POST['username']
    pswd = request.POST['password']

    user = authenticate(username=usr, password=pswd)
    if user:
        auth_login(request, user)
        return HttpResponseRedirect("/courses/")
    
    return render(request, "login.html", {"error": "username or password is wrong"})

def log_out(request):
    logout(request)
    return HttpResponseRedirect("/courses/login")