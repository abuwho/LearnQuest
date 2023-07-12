from .serializers_import import *
from .course_serializers import CartDisplayCourseSerializer

class DisplayCartSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying cart details.

    Fields:
        total_price (SerializerMethodField): The total price of the cart (read-only).
        item_count (SerializerMethodField): The number of items in the cart (read-only).
        courses (SerializerMethodField): The courses in the cart (read-only).

    Meta:
        model (Cart): The Cart model to serialize.
        fields (list): List of fields to include in the serialization.

    """
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
    """
    Serializer for adding a course to the cart.

    Fields:
        course (UUIDField): The UUID of the course to add to the cart.

    """
    course = serializers.UUIDField()

class RemoveFromCartSerializer(serializers.Serializer):
    """
    Serializer for removing a course from the cart.

    Fields:
        course (UUIDField): The UUID of the course to remove from the cart.

    """
    course = serializers.UUIDField()