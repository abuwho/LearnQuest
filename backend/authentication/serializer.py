from rest_framework import serializers
from .models import User
from learnquest.models import Profile

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
    
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only= True)
    
    class Meta:
        model = Profile
        fields = "__all__"
        
    def get_user(self, instance):
        return DisplayUserSerializer(instance=instance.user).data 
