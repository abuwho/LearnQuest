from serializers_import import *

class DisplayCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["total_price", "item_count"]