from django.contrib import admin
from django.urls import path, include
from .views import views


urlpatterns = [
    path("apply/", views.submit_instructor_application, name="submit-instructor-application"),
    path("courses/", views.get_all_courses, name="get-all-courses"),
    # path to create a course
    path("courses/create", views.create_course, name="create-course"),
    path("courses/create_section", views.create_section, name="create-section"),
    path("courses/update_section", views.update_section, name="update-section"),
    path("courses/delete_section", views.delete_section, name="delete-section")
]