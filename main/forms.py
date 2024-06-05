from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator, EmailValidator

from .models import Course, Comment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'price', 'creator', 'image']
        widgets = {
            "name": forms.TextInput(attrs={'placeholder': 'name'}),
            "description": forms.Textarea(attrs={'placeholder': 'description'}),
        }
        labels = {
            'name': "name",
            "description": "description",
        }


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'text'}),
                           validators=[MaxLengthValidator(100), MinLengthValidator(10)], label="Text")

    class Meta:
        model = Comment
        fields = ['text']


class SortingForm(forms.Form):
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'price'}))
    choice = forms.ChoiceField(choices=[
        ("lt", "Less than"),
        ("gt", "Greater than"),
        ("eq", "Equal to"),
    ])
    which = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                               required=False)
    choice1 = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), required=False)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username or email'}),
                               label="Username or Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}),validators=[
        MaxLengthValidator(100), MinLengthValidator(3)
    ])
    #captcha = CaptchaField()


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}), validators=[
        MaxLengthValidator(50), MinLengthValidator(3)
        , RegexValidator(
            r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&]{3,}$'
        )
    ])
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'email'}))
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'balance', 'photo']


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'email'}))
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'balance', 'photo']


class ChooseGroupForm(forms.Form):
    sliders = forms.ChoiceField(choices=[("Student", "Student"), ("Teacher", "Teacher"), ("Admin", "Admin")],
                                widget=forms.Select(attrs={'class': 'form-control'}))


class FullUpdateOfUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'balance']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'username'}),
            'email': forms.TextInput(attrs={'placeholder': 'email'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'balance': forms.NumberInput(attrs={'placeholder': 'balance'}),
        }
