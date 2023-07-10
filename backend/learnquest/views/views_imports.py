from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes,api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from learnquest.serializers.application_serializers import *
from learnquest.serializers.cart_serializers import *
from learnquest.serializers.course_serializers import *
from learnquest.serializers.lesson_serializers import *
from learnquest.serializers.review_serializers import *
from learnquest.serializers.section_serializers import *
from .application_views import *
from .cart_views import *
from .course_views import *
from .lesson_views import *
from .review_views import *
from .section_views import *