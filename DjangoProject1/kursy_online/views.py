import os

from lxml import etree

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.utils.xmlutils import SimplerXMLGenerator
from .models import Course, Subject, Message, User
from .forms import CourseForm, RegistrationForm, UserProfileForm
from django.db.models import Q
def home(request):
    if request.GET.get('q') is not None:
        q = request.GET.get('q')
    else:
        q = ""
    courses = Course.objects.filter(Q(subject__name__icontains=q) |
                                    Q(name__icontains=q) |
                                    Q(description__icontains=q)
                                    )

    if request.user.is_authenticated:
        user_courses = Course.objects.filter(students=request.user)
        teacher_courses = Course.objects.filter(teacher=request.user)
        recent_activities = Message.objects.filter(
            Q(course__in=user_courses) | Q(course__in=teacher_courses))
    else:
        recent_activities = Message.objects.none()


    subjects = Subject.objects.all()
    course_sum = courses.count()
    users_sum = User.objects.count()

    context = {"courses": courses, "subjects": subjects, "course_sum": course_sum, "users_sum": users_sum,
               "recent_activities": recent_activities}
    return render(request, 'kursy_online/home.html', context)


def course(request, p):
    course = Course.objects.get(id=p)
    students = course.students.all()
    comments = []
    if request.user in students or request.user == course.teacher:
        comments = course.message_set.all().order_by("-created")
    if request.method == "POST":
        if "comment" in request.POST and (request.user in students or request.user == course.teacher ):
            message = Message.objects.create(
                user=request.user,
                course=course,
                message=request.POST.get("comment"),
            )
            return redirect("course", p=course.id)
        elif "join_course" in request.POST and request.user != course.teacher:
            course.students.add(request.user)
            return redirect("course", p=course.id)
        elif "leave_course" in request.POST and request.user != course.teacher:
            course.students.remove(request.user)
            return redirect("course", p=course.id)
    context = {"course": course, "comments": comments, "students": students}

    return render(request, 'kursy_online/course.html', context)

@login_required(login_url="login")
def createCourse(request):
    form = CourseForm()
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
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
    return render(request, "kursy_online/login_registration/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")

def registerView(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            name = form.cleaned_data["name"]
            username = form.cleaned_data["username"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "An account with this username already exists.")
                return redirect("register")

            user = User.objects.create_user(name=name, username=username, email=email, password=password)

            token = default_token_generator.make_token(user)

            uid = urlsafe_base64_encode(str(user.pk).encode())

            # Prepare the email
            current_site = get_current_site(request)
            activation_link = f"http://{current_site.domain}/activate/{uid}/{token}/"
            subject = "Activate your account"
            message = render_to_string("kursy_online/login_registration/activation_email.html", {
                "user": user,
                "activation_link": activation_link,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

            # Redirect to the registration success page
            return redirect("registration_success")
    else:
        form = RegistrationForm()

    return render(request, "kursy_online/login_registration/register.html", {"form": form})


def activate_account(request, uidb64, token):
    try:
        # Decode the user ID (uid) from base64
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        # Check if the token matches
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated. You are now logged in.")

            # Log the user in automatically
            login(request, user)

            # Redirect to the user's dashboard or homepage
            return redirect('home')  # Replace with the URL where you want to redirect the logged-in user

        else:
            messages.error(request, "Invalid activation link.")
            return redirect('register')
    except (User.DoesNotExist, ValueError, OverflowError):
        messages.error(request, "Invalid activation link.")
        return redirect('register')

def registration_success(request):
    return render(request, "kursy_online/login_registration/registration_success.html")

@login_required(login_url="login")
def deleteMessage(request, p):
    message = Message.objects.get(id=p)
    course = message.course

    if request.user != message.user:
        return HttpResponse("You cannot do this!")

    if request.method == "POST":
        message.delete()
        return redirect("course", p=course.id)
    context = {"object": message}
    return render(request, "kursy_online/delete.html", context)




def viewProfile(request, p):
    user = get_object_or_404(User, id=p)

    created_courses_count = Course.objects.filter(teacher=user).count()
    join_courses_count = Course.objects.filter(students=user).count()

    if request.user.is_authenticated:
        user_courses = Course.objects.filter(students=request.user)
        teacher_courses = Course.objects.filter(teacher=request.user)
        recent_activities = Message.objects.filter(
            Q(course__in=user_courses) | Q(course__in=teacher_courses))
    else:
        recent_activities = Message.objects.none()

    if request.user == user and request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", p=user.id)
    else:
        form = UserProfileForm(instance=user)

    context = {
        "user": user,
        "created_courses_count": created_courses_count,
        "join_courses_count": join_courses_count,
        "recent_activities": recent_activities,
        "form": form if request.user == user else None,
    }
    return render(request, "kursy_online/profile.html", context)


def yourCourses(request, p):
    user = User.objects.get(id=p)
    created_courses = Course.objects.filter(teacher=user)
    joined_courses = Course.objects.filter(students=user)
    context = {"created_courses": created_courses, "joined_courses": joined_courses}
    return render(request, "kursy_online/your_courses.html", context)


def generate_courses_xml(courses, xslt_filename, output_filename):
    # funkcja pomocnicza, aby uniknąć redundancji
    if not courses.exists():
        return HttpResponse(f"<h1>No courses found.</h1>", content_type="text/html")

    root = etree.Element("courses")
    for course in courses:
        course_element = etree.SubElement(root, "course", id=str(course.id))
        etree.SubElement(course_element, "name").text = course.name
        etree.SubElement(course_element, "description").text = course.description or ""
        etree.SubElement(course_element, "teacher").text = course.teacher.name if course.teacher else "Unknown"
        etree.SubElement(course_element, "created").text = str(course.created)

    xslt_path = os.path.join("static", "xsl", xslt_filename)
    try:
        with open(xslt_path, "r") as xslt_file:
            xslt_root = etree.XML(xslt_file.read().encode('utf-8'))
    except FileNotFoundError:
        return HttpResponse("<h1>XSL file not found.</h1>", content_type="text/html")

    transform = etree.XSLT(xslt_root)
    result = transform(root)

    response = HttpResponse(
        str(result),
        content_type="application/xhtml+xml"
    )
    response['Content-Disposition'] = f'attachment; filename="{output_filename}"'
    return response

@login_required
def download_joined_courses_xml(request):
    joined_courses = Course.objects.filter(students=request.user)
    return generate_courses_xml(
        joined_courses,
        xslt_filename = "joined_courses.xsl",
        output_filename="joined_courses.html"
    )

@login_required
def download_created_courses_xml(request):
    created_courses = Course.objects.filter(teacher=request.user)
    return generate_courses_xml(
        created_courses,
        xslt_filename = "created_courses.xsl",
        output_filename="created_courses.html"
    )
