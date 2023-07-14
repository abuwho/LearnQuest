from .serializers_import import *

class RequestInstructorApplicationSerializer(serializers.Serializer):
    """
    Serializer for requesting instructor application.

    Fields:
        reason (CharField): The reason for requesting the instructor application.

    """
    reason = serializers.CharField()
    

class ResponseInstructorApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for the instructor application response.

    Meta:
        model (InstructorApplication): The InstructorApplication model to serialize.
        fields (list): List of fields to include in the serialization.

    """
    class Meta:
        model = InstructorApplication
        fields = "__all__"
        