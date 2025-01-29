from django.contrib import admin
from .models import Course, Subject, Message, User, CourseMaterial, TeacherRating

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Message)
admin.site.register(CourseMaterial)
admin.site.register(TeacherRating)

