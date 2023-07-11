from .serializers_import import *

class EnrolledViewLessonSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Lesson
        fields = ["id", "title", "duration", "section", "type", "pdf", "video_url", "summary",  "created_at", "updated_at"]
        
    def get_duration(self, instance):
        return instance.duration
    


class UnenrolledViewLessonSerializer(serializers.Serializer):
    duration = serializers.SerializerMethodField(read_only= True)
    class Meta:
        model = Lesson
        fields = ['id','title',"section", "duration"]
    
    def get_duration(self, instance):
        return instance.duration
    
class RequestCreateLessonSerializer(serializers.Serializer):
    title = serializers.CharField()
    section = serializers.UUIDField()
    type = serializers.CharField()
    pdf = serializers.FileField(required = False)
    video_url = serializers.URLField(required = False)
    summary = serializers.CharField(required = False)


class ResponseCreateLessonSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Lesson
        fields = "__all__"
        
    def get_duration(self, instance):
        return instance.duration


class RequestUpdateLessonSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    section = serializers.UUIDField()
    type = serializers.CharField()
    pdf = serializers.FileField(required = False)
    video_url = serializers.URLField(required = False)
    summary = serializers.CharField(required = False)
    

class ResponseUpdateLessonSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Lesson
        fields = "__all__"
        
    def get_duration(self, instance):
        return instance.duration