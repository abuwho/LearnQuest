from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from course.models import Course


@api_view(["GET"])
@permission_classes([AllowAny])
# Get all courses
def get_all_courses(request):
    data = request.data
    try:
        courses = Course.objects.all()
        return Response({
            "courses": courses,
        }, status=200)
    except Exception as e:
        return Response(
            {}, status=400
        )
    
