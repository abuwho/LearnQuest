from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("signup/", views.sign_up, name="signup"),
    path("login/", views.log_in, name="login"),
    path('get_current_user/', views.get_current_user, name= "get_current_user"), 
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("verify_forgot_password_code/<int:code>", views.verify_code, name="verify_forgot_password_code"),
    path("set_new_password/", views.set_new_password, name="set_new_password"),
    path("update_profile/", views.update_profile, name="update_profile"),
]