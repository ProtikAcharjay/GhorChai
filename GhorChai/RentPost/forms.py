from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'price', 'location', 'contact']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        # for built in model use touple not array
        model = User
        fields = ('username', 'email', 'password1', 'password2')