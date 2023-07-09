from .serializers_import import *
from .lesson_serializers import EnrolledViewLessonSerializer, UnenrolledViewLessonSerializer
class RequestCreateSectionSerializer(serializers.Serializer):
    title = serializers.CharField()
    course_id = serializers.UUIDField()
    
class ResponseCreateSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"
        
class RequestUpdateSectionSerializer(serializers.Serializer):
    title = serializers.CharField()
    
class ResponseUpdateSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"
        
class EnrolledViewSectionSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField(read_only = True)
    duration = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Section
        fields = ["duration", "lessons", "course", "title", "created_at", "updated_at"]
        
    def get_lessons(self,instance):
        lessons = instance.lessons
        return EnrolledViewLessonSerializer(instance=lessons, many = True).data
        


class UnenrolledViewSectionSerializer(serializers.Serializer):
    lessons = serializers.SerializerMethodField(read_only = True)
    duration = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Section
        fields = ["duration", "lessons", "course", "title", "created_at", "updated_at"]
        
    def get_lessons(self,instance):
        lessons = instance.lessons
        return UnenrolledViewLessonSerializer(instance=lessons, many = True).data


        
