from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class account(AbstractUser):
  groups = models.ManyToManyField(Group, related_name="custom_user_set")
  
  user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set")
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
