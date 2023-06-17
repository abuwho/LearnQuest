from rest_framework import serializers

class AuthLoginSeriaizer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=300, allow_blank=False, trim_whitespace=True, required=True)
    token = serializers.CharField(max_length=256, read_only=True)

class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=300, allow_blank=False, trim_whitespace=True, required=True)
    token = serializers.CharField(max_length=256, read_only=True)