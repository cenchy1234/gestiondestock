from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import User  # Custom User model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    pass
