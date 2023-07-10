from .serializers_import import *

class RequestInstructorApplicationSerializer(serializers.Serializer):
    reason = serializers.CharField()
    

class ResponseInstructorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorApplication
        fields = "__all__"
        