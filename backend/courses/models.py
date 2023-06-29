import uuid
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as q
from django.db import models


# Create your models here.

# Create a model class for `course`
class Course(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    instructor = models.ForeignKey("authentication.User", on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name
    

# Crate a model class for `lesson`
class Lesson(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    # content= models.TextField(null=False, blank=False)
    # video_link= models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name
    

# Create a model class for `review`
class Review(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=False, blank=False)
    rating = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review

# Create a model class for `category of courses`
class Category(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    image = models.FileField(upload_to="categoryPictures", default=None)

    def __str__(self):
        return self.name
