from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes,api_view, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializer import AuthLoginSerializer, AuthSerializer, ForgotPasswordSerializer, ProfileSerializer, ProfileUpdateSerializer
from django.contrib.auth import authenticate, login
from .utils import send_reset_email, validate_code
from knox.models import AuthToken
from rest_framework.parsers import FormParser, MultiPartParser
from learnquest.models import Profile

User = get_user_model()


@swagger_auto_schema(methods=['POST'], request_body=AuthLoginSerializer,
                     responses={201: AuthSerializer(), 400: {}})
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    data = request.data
    serialized = AuthLoginSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        email = serialized.data.get("email")
        password = serialized.data.get("password")
        print(password)
        if User.objects.filter(email=email).exists():
            created_user = User.objects.get(email=email)
            if created_user.is_active:
                raise ValueError("User already exists")
        else:
            created_user = User.objects.create(email=email, username=email.split("@")[0])
            created_user.set_password(password)
            # created_user.is_active = True # todo: When we want to implement the email verification
            created_user.save()
            token = AuthToken.objects.create(user=created_user)[1]
            login(request, created_user)
            return Response({
                "username": created_user.username,
                "email": created_user.email,
                "token": token,
            }, status=201)
    except Exception as e:
        return Response(
            {}, status=400
        )
        
@swagger_auto_schema(methods=['GET'],
                     responses={201: ProfileSerializer(), 400: {}})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    profile= Profile.objects.get(user= user)
    return Response(ProfileSerializer(profile).data, status=201)


@swagger_auto_schema(methods=['PUT'], request_body=ProfileUpdateSerializer, responses={201: ProfileSerializer(), 400: {}})
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def update_profile(request):
    data = request.data
    serialized = ProfileUpdateSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        profile = request.user.profile
        if "profile_picture" in serialized.validated_data:
            profile.profile_picture = serialized.validated_data.get("profile_picture")
        if "bio" in  serialized.validated_data:
            profile.bio = serialized.validated_data.get("bio")
        if "twitter" in serialized.validated_data:
            profile.twitter = serialized.validated_data.get("twitter")
        if "linkedIn" in serialized.validated_data:
            profile.linkedIn = serialized.validated_data.get("linkedIn")
        if "location" in serialized.validated_data:
            profile.location = serialized.validated_data.get("location")
        if "phoneNumber" in serialized.validated_data:
            profile.phoneNumber = serialized.validated_data.get("phoneNumber")
        if "first_name" in serialized.validated_data:
            profile.user.firstname = serialized.validated_data.get("first_name")
        if "last_name" in serialized.validated_data:
            profile.user.lastname = serialized.validated_data.get("last_name")
        profile.user.save()
        profile.save()
        return Response(ProfileSerializer(profile).data, status=201)
    except Exception as e:
        return Response(
            {"error": str(e)}, status=400
        )


@swagger_auto_schema(methods=['POST'], request_body=AuthLoginSerializer,
                     responses={201: AuthSerializer(), 400: {}})
@api_view(["POST"])
@permission_classes([AllowAny])
def log_in(request):
    data = request.data
    serialized = AuthLoginSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        # username = serialized.data.get("username")
        email = serialized.data.get("email")
        password = serialized.data.get("password")
        user = authenticate(username=email, password=password)
        print(f'email: {email}, password: {password}')
        print(user)
        if user is None:
            raise ValueError("Either user does not exist or the credentials are incorrect")
        else:
            token = AuthToken.objects.create(user=user)[1]
            login(request, user)
            return Response({
                "username": user.username,
                "email": user.email,
                "token": token,
            }, status=200)
    except Exception as e:
        return Response(
            {"error": str(e)}, status=400
        )
        
@swagger_auto_schema(methods=['POST'], request_body=ForgotPasswordSerializer,
                     responses={201: {}, 400: {}})
@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password(request):
    data = request.data
    serialized = ForgotPasswordSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        email = serialized.data.get("email")
        user = User.objects.get(email = email)
        if user is None:
            return Response({}, status= 404)
        send_reset_email(user)
        return Response({}, 200)
    except Exception as e:
        return Response(
            {"error": str(e)}, status=400
        )
        
@api_view(["POST"])
@permission_classes([AllowAny])
def verify_code(request, code):
    try:
        user = validate_code(code)
        if user is None:
            return Response({"error": "invalid code"}, status = 400)
        else:
            return Response({"email": user.email}, status = 200)
    except Exception as e:
        return Response(
            {"error": str(e)}, status=400
        )
        
@swagger_auto_schema(methods=['POST'], request_body=AuthLoginSerializer(),
                     responses={201: {}, 400: {}})
@api_view(["POST"])
@permission_classes([AllowAny])
def set_new_password(request):
    data = request.data
    serialized = ForgotPasswordSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        email = serialized.data.get("email")
        password = serialized.data.get("password")
        user = User.objects.get(email= email)
        if user is None:
            return Response({}, status= 404)
        else:
            user.set_password(password)
            user.save()
            return Response({}, status = 200)
    except Exception as e:
        return Response(
            {"error": str(e)}, status=400
        )