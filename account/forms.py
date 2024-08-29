from cloudinary.forms import CloudinaryFileField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import account 

class AccountCreationForm(UserCreationForm):
    class Meta:
        model = account
        fields = ('username','email', 'bio','profile_picture')



        
