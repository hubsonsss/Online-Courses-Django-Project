# Generated by Django 5.1.4 on 2025-01-13 19:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kursy_online", "0003_subject_course_teacher_messages_course_subject"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Messages",
            new_name="Message",
        ),
    ]
