from django.forms import ModelForm
from kursy_online.models import Course

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
