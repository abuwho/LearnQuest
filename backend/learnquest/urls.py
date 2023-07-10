from django.contrib import admin
from django.urls import path, include
from .views import views

urlpatterns = [
    path("apply/", views.submit_instructor_application, name="submit-instructor-application"),
    path("courses/", views.get_all_courses, name="get-all-courses"),
    path("courses/create", views.create_course, name="create-course"),
    path("courses/<str:course_id>/update", views.update_course, name="update-course"),
    path("courses/<str:course_id>/delete", views.delete_course, name="delete-course"),
    path("courses/<str:course_id>/preview", views.preview_course, name="preview-course"),
    path("courses/<str:course_id>/full_view", views.full_view_course, name="full-view-course"),
    path("courses/enrolled", views.get_enrolled_courses, name="get-enrolled-courses"),
    path("courses/created", views.get_created_courses, name="get-created-courses"),
    path("courses/get_lessons_in_section/<str:section_id>", views.get_all_lessons_in_section, name="get-all-lessons-in-section"),
    path("courses/create_section", views.create_section, name="create-section"),
    path("courses/update_section", views.update_section, name="update-section"),
    path("courses/delete_section", views.delete_section, name="delete-section"),
    path("courses/create_lesson", views.create_lesson, name="create-lesson"),
    path("courses/update_lesson", views.update_lesson, name="update-lesson"),
    path("courses/delete_lesson", views.delete_lesson, name="delete-lesson"),
    path("courses/review", views.create_review, name="create-review")
]
