from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Create, update, delete courses
    path("", views.CRUD_courses, name="CRUD_courses"),
    # path to get all courses
    path("all", views.get_courses, name="get_courses"),
    # path to get courses that a user has enrolled in only if they are authenticated
    path("my", views.get_my_courses, name="get_my_courses"),
    # path to get all courses by category as a string
    path("category/<str:category>", views.get_all_courses_by_category, name="get_all_courses_by_category"),
    # path to get a course by id
    path("<int:id>", views.get_course_by_id, name="get_course_by_id"),
    # path to get all lessons for a course
    path("<int:id>/lessons/all", views.get_lessons_by_course_id, name="get_lessons_by_course_id"),
    # path to create, update, delete lessons
    path("<int:id>/lessons", views.CRUD_lesson, name="CRUD_lessons"),
    # create, update, delete reviews
    path("<int:id>/reviews", views.CRUD_review, name="CRUD_reviews"),
    # path to get all reviews for a course
    path("<int:id>/reviews/all", views.get_reviews_by_course_id, name="get_reviews_by_course_id"),
]