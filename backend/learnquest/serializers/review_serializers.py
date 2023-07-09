from .serializers_import import *

class ViewReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        
class RequestCreateReviewSerializer(serializers.Serializer):
    course = serializers.UUIDField()
    rating = serializers.IntegerField()
    comment= serializers.CharField(required = False)
    
    
class ResponseCreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"