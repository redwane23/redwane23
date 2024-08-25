from cloudinary.forms import CloudinaryFileField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CreationForm(UserCreationForm):
    password=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = account
        fields = ('username','email', 'bio', 'password')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']



        
