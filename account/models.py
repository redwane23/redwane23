from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from cloudinary.models import CloudinaryField
from django.db import models

class account(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=50,unique=True)
  email = models.EmailField(unique=True,null=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  bio = models.CharField(max_length=200,blank=True)
  profile_picture = CloudinaryField('image', blank=True, null=True)
  
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  def __str__(self):
      return self.username
