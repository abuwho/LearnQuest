from .views_imports import *


# Get all courses
@swagger_auto_schema(method='GET', responses={200: UnauthorizedViewCourseSerializer(many=True)})
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_courses(request):
    courses = Course.objects.all()
    serialized = UnauthorizedViewCourseSerializer(courses, many=True)
    return Response(serialized.data, status=200)



# Create a course
@swagger_auto_schema(method='POST', request_body=RequestCreateCourseSerializer, responses={201: ResponseCreateCourseSerializer()})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course(request):
    data = request.data
    serialized = RequestCreateCourseSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        course = Course(title=serialized.validated_data.get("title"), instructor=request.user,
                        price=serialized.validated_data.get("price"),
                        description=serialized.validated_data.get("description"),
                        image=serialized.validated_data.get("image"))
        course.save()
        return Response(ResponseCreateCourseSerializer(course).data, status=201)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)
