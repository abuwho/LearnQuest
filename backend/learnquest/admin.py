


# Register your models here.
from django.contrib import admin
from learnquest.models import Profile, Lesson, Cart, Course, Section, InstructorApplication, Review, Wallet, CartCourse, CourseEnrollment

admin.site.register(Profile)
admin.site.register(Lesson)
admin.site.register(Cart)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(InstructorApplication)
admin.site.register(Review)
admin.site.register(Wallet)
admin.site.register(CourseEnrollment)
admin.site.register(CartCourse)
