from rest_framework import serializers
from .models import User
from learnquest.models import Profile, Wallet

class AuthLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=300, allow_blank=False, trim_whitespace=True, required=True)
    token = serializers.CharField(max_length=256, read_only=True)

class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=300, allow_blank=False, trim_whitespace=True, required=True)
    token = serializers.CharField(max_length=256, read_only=True)
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class SetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    
    
class DisplayUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "is_superuser", "is_staff", "groups", "user_permissions"]


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields ="__all__"
        
class TopUpSerializer(serializers.Serializer):
    amount = serializers.FloatField(required = True)

    
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only= True)
    wallet = serializers.SerializerMethodField(read_only= True)
    cart = serializers.SerializerMethodField(read_only= True)
    
    class Meta:
        model = Profile
        fields = ["id", "user", "wallet", "cart", "profile_picture", "bio", "twitter", "linkedIn", "location", "phoneNumber", "created_at", "updated_at"]
        
    def get_user(self, instance):
        return DisplayUserSerializer(instance=instance.user).data
    
    def get_wallet(self, instance):
        return WalletSerializer(instance.user.wallet).data
    

    def get_cart(self, instance):
        return instance.user.cart.id
    
class ProfileUpdateSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField(required=False)
    bio = serializers.CharField(required=False)
    twitter = serializers.URLField(required=False)
    linkedIn = serializers.URLField(required=False)
    location = serializers.CharField(required=False)
    phoneNumber = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    
