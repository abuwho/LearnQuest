from django.contrib import admin
from django.urls import path, include
from .views import views


urlpatterns = [
    path("apply/", views.submit_instructor_application, name="submit-instructor-application"),
]