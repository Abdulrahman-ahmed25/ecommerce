from django import forms
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    # to make the email unique
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_count = User.objects.filter(email = email).count()
        if user_count > 0:
            raise forms.ValidationError("this email already in use")
        return email

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2' ]
