from django.forms import ModelForm
from django import forms

from kursy_online.models import Course, User


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        exclude = ["teacher", "students"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'image', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class RegistrationForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50, required=True)
    username = forms.CharField(label="Username", max_length=50, required=True)
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data