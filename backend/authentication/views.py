from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializer import AuthLoginSeriaizer, AuthSerializer
from django.contrib.auth import authenticate, login
from knox.models import AuthToken


User = get_user_model()


@swagger_auto_schema(methods=['POST'], request_body=AuthLoginSeriaizer,
                     responses={201: AuthSerializer(), 400: {}})
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_up(request):
    data = request.data
    serialized = AuthLoginSeriaizer(data=data)
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
