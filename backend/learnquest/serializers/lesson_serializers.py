from .serializers_import import *

class EnrolledViewLessonSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying enrolled lesson details.

    Fields:
        duration (SerializerMethodField): The duration of the lesson (read-only).

    Meta:
        model (Lesson): The Lesson model to serialize.
        fields (list): List of fields to include in the serialization.

    """
    duration = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Lesson
        fields = ["id", "title", "duration", "section", "type", "pdf", "video_url", "summary",  "created_at", "updated_at"]
        
    def get_duration(self, instance):
        return instance.duration
    

class UnenrolledViewLessonSerializer(serializers.Serializer):
    """
    Serializer for displaying unenrolled lesson details.

    Fields:
        duration (SerializerMethodField): The duration of the lesson (read-only).

    Meta:
        model (Lesson): The Lesson model to serialize.
        fields (list): List of fields to include in the serialization.
    """
    duration = serializers.SerializerMethodField(read_only= True)
    class Meta:
        model = Lesson
        fields = ['id','title',"section", "duration"]
    
    def get_duration(self, instance):
        return instance.duration


class RequestCreateLessonSerializer(serializers.Serializer):
    """
    Serializer for creating a lesson.

    Fields:
        title (CharField): The title of the lesson.
        section (UUIDField): The UUID of the section the lesson belongs to.
        type (CharField): The type of the lesson (either "video" or "pdf").
        pdf (FileField): The PDF file of the lesson (required if type is "pdf").
        video_url (URLField): The URL of the video of the lesson (required if type is "video").
        summary (CharField): The summary of the lesson.
    """
    title = serializers.CharField()
    section = serializers.UUIDField()
    type = serializers.CharField()
    pdf = serializers.FileField(required = False)
    video_url = serializers.URLField(required = False)
    summary = serializers.CharField(required = False)


class ResponseCreateLessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the lesson response.

    Fields:
        duration (SerializerMethodField): The duration of the lesson (read-only).

    Meta:
        model (Lesson): The Lesson model to serialize.
        fields (list): List of fields to include in the serialization.
    """
    duration = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Lesson
        fields = "__all__"
        
    def get_duration(self, instance):
        return instance.duration


class RequestUpdateLessonSerializer(serializers.Serializer):
    """
    Serializer for updating a lesson.

    Fields:
        title (CharField): The title of the lesson.
        section (UUIDField): The UUID of the section the lesson belongs to.
        type (CharField): The type of the lesson (either "video" or "pdf").
        pdf (FileField): The PDF file of the lesson (required if type is "pdf").
        video_url (URLField): The URL of the video of the lesson (required if type is "video").
        summary (CharField): The summary of the lesson.
    """
    id = serializers.UUIDField()
    title = serializers.CharField()
    section = serializers.UUIDField()
    type = serializers.CharField()
    pdf = serializers.FileField(required = False)
    video_url = serializers.URLField(required = False)
    summary = serializers.CharField(required = False)
    

class ResponseUpdateLessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the lesson response.

    Fields:
        duration (SerializerMethodField): The duration of the lesson (read-only).

    Meta:
        model (Lesson): The Lesson model to serialize.
        fields (list): List of fields to include in the serialization.
    """
    duration = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Lesson
        fields = "__all__"
        
    def get_duration(self, instance):
        return instance.duration