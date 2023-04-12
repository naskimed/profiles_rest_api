# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.models import BaseUserManager


from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model."""
    
    def create_user(self,email,name,password):
        """Create a new user profile object."""

        if not email:
            raise ValueError("user must have an email adress")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using = self._db)

        return user 
    
    def create_superuser(self,email,name,password):
        """Creates and saves new superuser with given details"""

        user = self.create_user(email,name,password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user 


class UserProfiles(AbstractBaseUser, PermissionsMixin):
    """"Represnt a user_profile inside our system """

    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """"Used to get a users full name"""

        return(self.name)
    
    def get_short_name(self):
        """Used to get a users short name."""

        return self.name
    
    def __str__(self):
        """"Django uses this when it needs to convert the object to a string"""
        return self.email  
    
class Superuser(AbstractUser):
    pass
    
class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    superuser = models.ForeignKey(Superuser, on_delete=models.CASCADE)
    users = models.ManyToManyField(UserProfiles, through='UserGroup')

class UserGroup(models.Model):
    user = models.ForeignKey(UserProfiles, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Subject(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    groups = models.ManyToManyField(Group, through='GroupSubject')

class GroupSubject(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)