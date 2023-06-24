from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path to get all courses
    path("", views.get_all_courses, name="get_all_courses"),
    # path to get a course by id
    path("<int:id>", views.get_course_by_id, name="get_course_by_id"),
    # path to get all lessons in a course
    path("<int:id>/lessons", views.get_lessons_by_course_id, name="get_lessons_by_course_id"),
    # path to get a lesson by id
    path("<int:id>/lessons/<int:lesson_id>", views.get_lesson_by_id, name="get_lesson_by_id"),
]
