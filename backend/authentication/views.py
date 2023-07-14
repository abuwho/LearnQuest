from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes,api_view, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializer import AuthLoginSerializer, AuthSerializer, ForgotPasswordSerializer, ProfileSerializer, ProfileUpdateSerializer,TopUpSerializer 
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
    """
    Sign up a new user.

    This view function handles the sign-up process for a new user. It creates a new user with the provided email and password,
    and returns a response with the user details and authentication token upon successful sign-up.

    Request:
        method: POST
        body: AuthLoginSerializer

    Responses:
        - 201: AuthSerializer - The user details and authentication token upon successful sign-up.
        - 400: An empty response indicating a bad request.

    """
    data = request.data
    serialized = AuthLoginSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        email = serialized.data.get("email")
        password = serialized.data.get("password")
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
    """
    Get the details of the current authenticated user.

    This view function retrieves the details of the current authenticated user, including their profile information,
    and returns a response with the serialized profile data.

    Request:
        method: GET

    Responses:
        - 201: ProfileSerializer - The serialized profile data of the current authenticated user.
        - 400: An empty response indicating a bad request.

    """
    user = request.user
    profile= Profile.objects.get(user= user)
    return Response(ProfileSerializer(profile).data, status=201)


@swagger_auto_schema(methods=['PUT'], request_body=ProfileUpdateSerializer, responses={201: ProfileSerializer(), 400: {}})
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def update_profile(request):
    """
    Update the profile of the current authenticated user.

    This view function updates the profile of the current authenticated user based on the provided data in the request.
    It uses the ProfileUpdateSerializer for validation and updates the corresponding fields in the user's profile.

    Request:
        method: PUT
        body: ProfileUpdateSerializer

    Responses:
        - 201: ProfileSerializer - The serialized profile data of the updated profile.
        - 400: An error response indicating a bad request.

    """
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
    

@swagger_auto_schema(methods=['POST'],request_body=TopUpSerializer,
                     responses={201: ProfileSerializer(), 400: {}})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def topup(request):
    """
    Top up the user's wallet balance.

    This view function handles the top-up process for the user's wallet balance. It validates the provided amount,
    adds the amount to the user's wallet balance, and returns the updated profile data.

    Request:
        method: POST
        body: TopUpSerializer

    Responses:
        - 201: ProfileSerializer - The serialized profile data of the user after the top-up.
        - 400: An error response indicating a bad request.

    """
    data = request.data
    serialized = TopUpSerializer(data = data)
    try:
        serialized.is_valid(raise_exception=True)
        amount = serialized.validated_data.get("amount")
        if amount < 0:
            return Response({"message":"Amount should be positive", "error": ""}, status = 400)
        wallet = request.user.wallet
        wallet.balance += amount
        wallet.save()
        profile = Profile.objects.get(user = request.user)
        return Response(ProfileSerializer(profile).data, status = 200)
    except Exception as e:
        return Response(
            {"message": "Something went wrong","error": str(e)}, status=400
        )


@swagger_auto_schema(methods=['POST'], request_body=AuthLoginSerializer,
                     responses={201: AuthSerializer(), 400: {}})
@api_view(["POST"])
@permission_classes([AllowAny])
def log_in(request):
    """
    Log in a user.

    This view function handles the login process for a user. It authenticates the provided credentials,
    generates an authentication token, and returns a response with the user details and token upon successful login.

    Request:
        method: POST
        body: AuthLoginSerializer

    Responses:
        - 201: AuthSerializer - The user details and authentication token upon successful login.
        - 400: An error response indicating a bad request.

    """
    data = request.data
    serialized = AuthLoginSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        # username = serialized.data.get("username")
        email = serialized.data.get("email")
        password = serialized.data.get("password")
        user = authenticate(username=email, password=password)
        print(f'email: {email}')
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
    """
    Initiate the password reset process.

    This view function initiates the password reset process by sending a reset email to the user's email address.

    Request:
        method: POST
        body: ForgotPasswordSerializer

    Responses:
        - 201: An empty response indicating a successful initiation of the password reset process.
        - 400: An error response indicating a bad request.

    """
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
    """
    Verify the password reset code.

    This view function verifies the provided password reset code and returns the email address associated with the code.

    Request:
        method: POST
        path parameter: code - The password reset code.

    Responses:
        - 200: {"email": str} - The email address associated with the code.
        - 400: An error response indicating an invalid code.

    """
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

      
@swagger_auto_schema(methods=['POST'], request_body=AuthLoginSerializer,
                     responses={201: {}, 400: {}})
@api_view(["POST"])
@permission_classes([AllowAny])
def set_new_password(request):
    """
    Set a new password for the user.

    This view function allows the user to set a new password by providing the email address and the new password.

    Request:
        method: POST
        body: AuthLoginSerializer

    Responses:
        - 201: An empty response indicating a successful password update.
        - 400: An error response indicating a bad request.

    """
    data = request.data
    serialized = AuthLoginSerializer(data=data)
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
            return Response({
                "username": user.username,
                "email": user.email,
            }, status=200)
    except Exception as e:
        return Response(
            {"error": str(e)}, status=400
        )