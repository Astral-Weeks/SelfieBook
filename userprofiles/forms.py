from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from .models import Selfies, Profile

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address already exists.')
        return email

class DateInput(forms.DateInput):
    input_type = 'date'

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'location', 'birthday']
        widgets = {
            'birthday': DateInput(),
        }

class UploadSelfieForm(forms.ModelForm):
    class Meta:
        model = Selfies
        fields = ['selfie', 'date', 'caption']
        widgets = {
            'date': DateInput(),
        }