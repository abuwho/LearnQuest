from .serializers_import import *
from .course_serializers import CartDisplayCourseSerializer

class DisplayCartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(read_only = True)
    item_count= serializers.SerializerMethodField(read_only = True)
    courses = serializers.SerializerMethodField(read_only = True) 
    class Meta:
        model = Cart
        fields = ["id","total_price", "item_count", "courses", "created_at", "updated_at"]
        
    def get_total_price(self, instance):
        return instance.total_price
    
    def get_item_count(self, instance):
        return instance.item_count
    
    def get_courses(self, instance):
        return CartDisplayCourseSerializer(instance=instance.courses, many = True).data
    
    

class AddToCartSerializer(serializers.Serializer):
    course = serializers.UUIDField()
    cart = serializers.UUIDField()
    
    