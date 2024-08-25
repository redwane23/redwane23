from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

class account(AbstractBaseUser, PermissionsMixin):
  username = CharField(max_lenght=50)
  email = EmailField(unique=True,null=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  bio = CharField(max_lenght=200)
  password = CharField(max_lenght=25)
  
