from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    # path to get all courses
    path("courses/", views.get_all_courses, name="get_all_courses"),
]