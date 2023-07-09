from .serializers_import import *

class EnrolledViewLessonSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Lesson
        fields = ["title", "duration", "section", "type", "pdf", "video_url", "created_at", "updated_at"]
        
    def get_duration(self, instance):
        return instance.duration
    


class UnenrolledViewLessonSerializer(serializers.Serializer):
    duration = serializers.SerializerMethodField(read_only= True)
    class Meta:
        model = Lesson
        fields = ['title',"section", "duration"]
    
    def get_duration(self, instance):
        return instance.duration