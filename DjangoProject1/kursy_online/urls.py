from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("course/<int:p>/", views.course, name="course"),
    path("create_course/", views.createCourse, name="create_course"),
    path("update_course/<int:p>", views.updateCourse, name="update_course"),
    path("delete_course/<int:p>", views.deleteCourse, name="delete_course"),
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerView, name="register"),
]
