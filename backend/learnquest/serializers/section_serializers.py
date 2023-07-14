from .serializers_import import *
from .lesson_serializers import EnrolledViewLessonSerializer, UnenrolledViewLessonSerializer
class RequestCreateSectionSerializer(serializers.Serializer):
    """
    Serializer for creating a section.

    Fields:
        title (CharField): The title of the section.
        course (UUIDField): The UUID of the course the section belongs to.

    """
    title = serializers.CharField()
    course = serializers.UUIDField()
    
class ResponseCreateSectionSerializer(serializers.ModelSerializer):
    """
    Serializer for the section response.

    Meta:
        model (Section): The Section model to serialize.
        fields (list): List of fields to include in the serialization.

    """
    class Meta:
        model = Section
        fields = "__all__"
        
class RequestUpdateSectionSerializer(serializers.Serializer):
    """
    Serializer for updating a section.

    Fields:
        title (CharField): The title of the section.
        section (UUIDField): The UUID of the section to update.

    """
    title = serializers.CharField()
    section = serializers.UUIDField()
    
class ResponseUpdateSectionSerializer(serializers.ModelSerializer):
    """
    Serializer for the section response.

    Meta:
        model (Section): The Section model to serialize.
        fields (list): List of fields to include in the serialization.

    """
    class Meta:
        model = Section
        fields = "__all__"

class RequestViewSectionSerializer(serializers.Serializer):
    """
    Serializer for viewing a section.

    Fields:
        course (UUIDField): The UUID of the course.

    """
    course = serializers.UUIDField()

class EnrolledViewSectionSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing a section.

    Fields:
        lessons (SerializerMethodField): The lessons of the section (read-only).
        duration (SerializerMethodField): The duration of the section (read-only).

    Meta:
        model (Section): The Section model to serialize.
        fields (list): List of fields to include in the serialization.

    """
    lessons = serializers.SerializerMethodField(read_only = True)
    duration = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Section
        fields = ["id", "duration", "lessons", "course", "title", "created_at", "updated_at"]
        
    def get_lessons(self,instance):
        lessons = instance.lessons
        return EnrolledViewLessonSerializer(instance=lessons, many = True).data
    
    def get_duration(self, instance):
        return instance.duration

class UnenrolledViewSectionSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing a section.

    Fields:
        lessons (SerializerMethodField): The lessons of the section (read-only).
        duration (SerializerMethodField): The duration of the section (read-only).

    Meta:
        model (Section): The Section model to serialize.
        fields (list): List of fields to include in the serialization.
        
    """
    lessons = serializers.SerializerMethodField(read_only = True)
    duration = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Section
        fields = ["id", "duration", "lessons", "course", "title", "created_at", "updated_at"]
        
    def get_lessons(self,instance):
        lessons = instance.lessons
        return UnenrolledViewLessonSerializer(instance=lessons, many = True).data
    
    def get_duration(self, instance):
        return instance.duration

class RequestDeleteSectionSerializer(serializers.Serializer):
    """
    Serializer for deleting a section.

    Fields:
        section (UUIDField): The UUID of the section to delete.

    """
    section = serializers.UUIDField()
