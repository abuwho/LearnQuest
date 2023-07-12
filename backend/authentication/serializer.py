from rest_framework import serializers
from .models import User
from learnquest.models import Profile, Wallet

class AuthLoginSerializer(serializers.Serializer):
    """
    Serializer for user authentication login.
    
    Fields:
        email (EmailField): The email address of the user (required).
        password (CharField): The password of the user (max length 300, cannot be blank or contain only whitespace, required).
        token (CharField): The authentication token for the user (max length 256, read-only).

    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=300, allow_blank=False, trim_whitespace=True, required=True)
    token = serializers.CharField(max_length=256, read_only=True)


class AuthSerializer(serializers.Serializer):
    """
    Serializer for user authentication.

    Fields:
        email (EmailField): The email address of the user (required).
        username (CharField): The username of the user (max length 300, cannot be blank or contain only whitespace, required).
        token (CharField): The authentication token for the user (max length 256, read-only).
    """
    email = serializers.EmailField(required=True)
    username = serializers.CharField(max_length=300, allow_blank=False, trim_whitespace=True, required=True)
    token = serializers.CharField(max_length=256, read_only=True)


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for user authentication.

    Fields:
        email (EmailField): The email address of the user (required).
    """
    email = serializers.EmailField(required=True)



class SetPasswordSerializer(serializers.Serializer):
    """
    Serializer for user authentication.

    Fields:
        email (EmailField): The email address of the user (required).
    """
    email = serializers.EmailField(required = True)

    
    
class DisplayUserSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying user details.

    Meta:
        model (User): The User model to serialize.
        exclude (list): List of fields to exclude from serialization.
    """
    class Meta:
        model = User
        exclude = ["password", "is_superuser", "is_staff", "groups", "user_permissions"]


class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for the Wallet model.

    Meta:
        model (Wallet): The Wallet model to serialize.
        fields (list): The fields to include in the serialization (all fields).

    """
    class Meta:
        model = Wallet
        fields ="__all__"
        
class TopUpSerializer(serializers.Serializer):
    """
    Serializer for topping up the Wallet.

    Fields:
        amount (FloatField): The amount to be topped up (required).

    """
    amount = serializers.FloatField(required = True)

    
class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.

    Fields:
        user (SerializerMethodField): Method field to serialize the associated user.
        wallet (SerializerMethodField): Method field to serialize the associated wallet.
        cart (SerializerMethodField): Method field to serialize the associated cart.

    Meta:
        model (Profile): The Profile model to serialize.
        fields (list): List of fields to include in the serialization.

    """
    user = serializers.SerializerMethodField(read_only= True)
    wallet = serializers.SerializerMethodField(read_only= True)
    cart = serializers.SerializerMethodField(read_only= True)
    
    class Meta:
        model = Profile
        fields = ["id", "user", "wallet", "cart", "profile_picture", "bio", "twitter", "linkedIn", "location", "phoneNumber", "created_at", "updated_at"]
        
    def get_user(self, instance):
        """
        Serialize the associated user.

        Args:
            instance (Profile): The Profile instance.

        Returns:
            dict: The serialized user.

        """
        return DisplayUserSerializer(instance=instance.user).data
    
    def get_wallet(self, instance):
        """
        Serialize the associated wallet.

        Args:
            instance (Profile): The Profile instance.

        Returns:
            dict: The serialized wallet.

        """
        return WalletSerializer(instance.user.wallet).data
    

    def get_cart(self, instance):
        """
        Serialize the associated cart.

        Args:
            instance (Profile): The Profile instance.

        Returns:
            int: The ID of the associated cart.

        """
        return instance.user.cart.id
    
class ProfileUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating the Profile model.

    Fields:
        profile_picture (ImageField): The profile picture (optional).
        bio (CharField): The bio (optional).
        twitter (URLField): The Twitter URL (optional).
        linkedIn (URLField): The LinkedIn URL (optional).
        location (CharField): The location (optional).
        phoneNumber (CharField): The phone number (optional).
        first_name (CharField): The first name (optional).
        last_name (CharField): The last name (optional).

    """
    profile_picture = serializers.ImageField(required=False)
    bio = serializers.CharField(required=False)
    twitter = serializers.URLField(required=False)
    linkedIn = serializers.URLField(required=False)
    location = serializers.CharField(required=False)
    phoneNumber = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
