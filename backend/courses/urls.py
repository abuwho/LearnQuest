from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Create, update, delete courses
    path("", views.CRUD_courses, name="CRUD_courses"),
    # path to get all courses
    path("all", views.get_courses, name="get_courses"),
    # path to get all courses by category as a string
    path("category/<str:category>", views.get_all_courses_by_category, name="get_all_courses_by_category"),
    # path to get a course by id
    path("<int:id>", views.get_course_by_id, name="get_course_by_id"),
    # path to get all lessons in a course
    path("<int:id>/lessons", views.get_lessons_by_course_id, name="get_lessons_by_course_id"),
    # path to get a lesson by id
    path("<int:id>/lessons/<int:lesson_id>", views.get_lesson_by_id, name="get_lesson_by_id"),
    # path to get all reviews in a course
    path("<int:id>/reviews", views.get_reviews_by_course_id, name="get_reviews_by_course_id"),
    # path to get a review by id
    path("<int:id>/reviews/<int:review_id>", views.get_review_by_id, name="get_review_by_id"),
    # path to get courses that a user has enrolled in only if they are authenticated
    path("my", views.get_my_courses, name="get_my_courses"),
]