from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager ,  Group
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class account(AbstractBaseUser):
  groups = models.ManyToManyField(Group, related_name="custom_user_set")
  
  user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set")
  username = models.CharField(max_length=50,unique=True)
  email = models.EmailField(unique=True,null=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  bio = models.CharField(max_length=200,blank=True)
  profile_picture = CloudinaryField('image', blank=True, null=True)

  objects = CustomUserManager()
  
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  def __str__(self):
      return self.username
