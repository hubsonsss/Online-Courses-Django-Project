from django.contrib import admin
from .models import Course, Subject, Message, User

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Message)
