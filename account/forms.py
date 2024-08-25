from django import forms
from django.contrib.auth.models import User
from cloudinary.forms import CloudinaryImageField

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    profile_picture = CloudinaryImageField()
    class Meta:
        model = User
        fields = ['username','profile_picture']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
