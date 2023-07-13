from .serializers_import import *

class ViewReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying review details.

    Fields:
        user (SerializerMethodField): The user who wrote the review (read-only).

    Meta:
        model (Review): The Review model to serialize.
        fields (list): List of fields to include in the serialization.
    """
    class Meta:
        model = Review
        fields = "__all__"
        
class RequestCreateReviewSerializer(serializers.Serializer):
    """
    Serializer for creating a review.

    Fields:
        course (UUIDField): The UUID of the course the review belongs to.
        rating (IntegerField): The rating of the course.
        comment (CharField): The comment of the review (optional).

    """
    course = serializers.UUIDField()
    rating = serializers.IntegerField()
    comment= serializers.CharField(required = False)
    
    
class ResponseCreateReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the review response.

    Meta:
        model (Review): The Review model to serialize.
        fields (list): List of fields to include in the serialization.
    """
    class Meta:
        model = Review
        fields = "__all__"