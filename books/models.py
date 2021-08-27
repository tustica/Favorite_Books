from django.db import models
from django.db.models.base import Model
import re
from datetime import datetime, timedelta

from django.db.models.deletion import CASCADE


class UserManager(models.Manager):
    def login_validator(request, postData):
        errors = {}
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex, postData['email'])):
            errors['email'] = "Invalid email"
        user = User.objects.filter(email=postData['email'])
        if user:
            errors['email'] = "Email already in use"
        return errors

    def validator(request, postData):
        errors = {}
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex, postData['email'])):
            errors['email'] = "Invalid email"
        user = User.objects.filter(email=postData['email'])
        if user:
            errors['email'] = "Email already in use"
        else:
            print('this is a new user')
        if len(postData['first_name'])<2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['last_name'])<2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if len(postData['password'])<8:
            errors['password'] = "Password must be longer than 8 characters"
        if postData['password']!= postData['confirm_pass']:
            errors['confirm_pass'] = "Passwords do not match"
        return errors


# User Model

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(request, postData):
        errors = {}
        if len(postData['title'])<2:
            errors['title'] = "Title must be longer than 2 characters"
        if len(postData['description'])>0 and len(postData['description'])<15:
            errors['description'] = "Description must be longer than 15 characters"
        return errors

#Book Model

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default="Book Description")
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=CASCADE)
    users_who_liked = models.ManyToManyField(User, related_name="books_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()