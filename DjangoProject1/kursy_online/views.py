from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Course, Subject, Message
from .forms import CourseForm
from django.db.models import Q
def home(request):
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    else:
        q = ""
    courses = Course.objects.filter(Q(subject__name__icontains=q) |
                                    Q(name__icontains=q) |
                                    Q(description__icontains=q)
                                    )
    subjects = Subject.objects.all()
    course_sum = courses.count()

    context = {"courses": courses, "subjects": subjects, "course_sum": course_sum}
    return render(request, 'kursy_online/home.html', context)

def course(request, p):
    course = Course.objects.get(id=p)
    comments = course.message_set.all().order_by("-created")

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            course=course,
            message=request.POST.get("comment"),
        )
        return redirect("course", p=course.id)
    context = {"course": course, "comments": comments}

    return render(request, 'kursy_online/course.html', context)

@login_required(login_url="login")
def createCourse(request):
    form = CourseForm()
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request,"kursy_online/course_appearance.html", context)


@login_required(login_url="login")
def updateCourse(request, p):
    course = Course.objects.get(id=p)
    form = CourseForm(instance=course)

    if request.user != course.teacher:
        return HttpResponse("You cannot do this!")

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "kursy_online/course_appearance.html", context)

@login_required(login_url="login")
def deleteCourse(request, p):
    course = Course.objects.get(id=p)

    if request.user != course.teacher:
        return HttpResponse("You cannot do this!")

    if request.method == "POST":
        course.delete()
        return redirect("home")
    context = {"object": course}
    return render(request, "kursy_online/delete.html", context)

def loginView(request):
    status = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, "Username not found")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid password")
    context = {"status": status}
    return render(request, "kursy_online/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")

def registerView(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username already exists")
    context = {"form": form}
    return render(request, "kursy_online/register.html", context)