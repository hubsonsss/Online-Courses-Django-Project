import re

from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
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
    name = forms.CharField(
        label="Name",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'Enter your full name'
        })
    )
    username = forms.CharField(
        label="Username",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'Enter a username'
        })
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'Enter your email address'
        })
    )
    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Enter a password'
        })
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        required=True,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Confirm your password'
        })
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not re.match(r'^[a-zA-Z]+$', name):
            raise ValidationError("Name must contain only letters.")

        return name

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another one.")

        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class PasswordResetConfirmForm(forms.Form):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        label="New Password",
        min_length=8
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label="Confirm Password",
        min_length=8
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 != password2:
            raise forms.ValidationError("The two password fields must match.")

        return cleaned_data