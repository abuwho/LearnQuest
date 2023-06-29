from rest_framework import serializers

from authentication.serializer import DisplayUserSerializer
from .models import Course, Review
class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model=Course
        fields="__all__"

    def get_user(self, instance):
        instructor = instance.instructor
        return DisplayUserSerializer(data  = instructor).data

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only = True)
    course = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model=Course
        fields="__all__"
    def get_user(self, instance):
        user = instance.user
        return DisplayUserSerializer(data  = user).data
    def get_course(self,instance):
         course=instance.course
         return CourseSerializer(data= course).data