from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("course/<int:p>/", views.course, name="course"),
    path("create_course/", views.createCourse, name="create_course"),
    path("update_course/<int:p>", views.updateCourse, name="update_course"),
    path("delete_course/<int:p>", views.deleteCourse, name="delete_course"),
    path("delete_message/<int:p>", views.deleteMessage, name="delete_message"),
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerView, name="register"),
    path("profile/<int:p>", views.viewProfile, name="profile"),
    path("your_courses/<int:p>", views.yourCourses, name="your_courses"),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='kursy_online/password_reset/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='kursy_online/password_reset/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='kursy_online/password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='kursy_online/password_reset/password_reset_complete.html'), name='password_reset_complete'),
    path('download-created-courses-xml/', views.download_created_courses_xml, name='download_created_courses_xml'),
    path('download-joined-courses-xml/', views.download_joined_courses_xml, name='download_joined_courses_xml'),
]
