import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    name = models.CharField(max_length=50, null=True, unique=True)
    email = models.EmailField()
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, default='avatar.png')
    is_active = models.BooleanField(default=False)
    activation_token = models.UUIDField(default=uuid.uuid4, editable=False)

    REQUIRED_FIELDS = ['email', 'name']

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(User, related_name='students', blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", '-created']

    def __str__(self):
        return self.name




class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", '-created']

    def __str__(self):
        return self.message[0:40]

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='course_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title