from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

import secrets

from api.models import ApiKey


class UserManager(BaseUserManager):
    def create_user(self, email):
        user = User()
        user.email = self.normalize_email(email)
        user.set_unusable_password()
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email=self.normalize_email(email))
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    
    objects = UserManager()