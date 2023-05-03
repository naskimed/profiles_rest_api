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
    

class Subject(models.Model):    
    """The Subject class"""

    Subname = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    students = models.ManyToManyField(UserProfiles, related_name='subjects')

    def __str__(self):
        return self.Subname

    def get_student_count(self):
        return self.students.count()
    

class Group(models.Model):
    """The group class which put the students of each class togother"""


    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(UserProfiles, related_name='group')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='group')

    def __str__(self):
        return self.name

    def get_member_count(self):
        return self.members.count()

    def add_member(self, user_profile):
        self.members.add(user_profile)

    def remove_member(self, user_profile):
        self.members.remove(user_profile)


