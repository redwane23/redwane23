from cloudinary.forms import CloudinaryFileField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import account 

class AccountCreationForm(UserCreationForm):
    password=forms.CharField(label='password',widget=forms.PasswordInput)
    password2=forms.CharField(label="confirm password",widget=forms.PasswordInput)
    
    class Meta:
        model = account
        fields = ('username','email', 'bio','profile_picture')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']



        
