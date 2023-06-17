import random
import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as q
from django.db import models


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(q('The Email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("firstname", "David")
        extra_fields.setdefault("username", str(random.randint(1, 999999)))
        extra_fields.setdefault("lastname", "Eje")

        if extra_fields.get('is_staff') is not True:
            raise ValueError(q('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(q('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(q("email address"), unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True)
    firstname = models.CharField(max_length=50, blank=True)
    lastname = models.CharField(max_length=50, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    roleChoices = [("student", "student"), ("instructor", "instructor")]
    role = models.CharField(choices=roleChoices, max_length=150, null=False, blank=False, default="student")
    is_active = models.BooleanField(default=True)
    account_status = models.CharField(max_length=256,
                                      choices=[("Active", "Active"), ("Blocked", "Blocked"), ("Admin", "Admin")],
                                      default="Active"
                                      )
    google_user = models.BooleanField(default=False)
    apple_user = models.BooleanField(default=False)
    image = models.FileField(upload_to="profilePictures", default=None)
    location = models.CharField(max_length=200, blank=True)
    phoneNumber = models.CharField(max_length=20, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username
