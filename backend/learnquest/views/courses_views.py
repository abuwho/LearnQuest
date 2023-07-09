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
@parser_classes([FormParser, MultiPartParser])
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


# Update a course
@swagger_auto_schema(method='PUT', request_body=RequestUpdateCourseSerializer, responses={200: ResponseUpdateCourseSerializer()})
@api_view(['PUT'])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def update_course(request, course_id):
    data = request.data
    serialized = RequestUpdateCourseSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        course = Course.objects.get(id=course_id)
        if course.instructor != request.user:
            return Response({"message": "Unauthorized: You are not the instructor of this course"}, status=401)
        
        # Update the course
        if serialized.validated_data.get("title") is not None:
            course.title = serialized.validated_data.get("title")
        if serialized.validated_data.get("price") is not None:
            course.price = serialized.validated_data.get("price")
        if serialized.validated_data.get("description") is not None:
            course.description = serialized.validated_data.get("description")
        if serialized.validated_data.get("image") is not None:
            course.image = serialized.validated_data.get("image")

        course.save()
        return Response(ResponseUpdateCourseSerializer(course).data, status=200)

    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)
    

# Delete a course
@swagger_auto_schema(method='DELETE', responses={200: {}})
@api_view(['DELETE'])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def delete_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        if course.instructor != request.user:
            return Response({"message": "Unauthorized: You are not the instructor of this course"}, status=401)
        course.delete()
        return Response({"message": "Course deleted successfully"}, status=200)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)
    


# Get all enrolled courses
@swagger_auto_schema(method='GET', responses={200: AuthorizedViewCourseSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_enrolled_courses(request):
    courses = Course.objects.filter(students=request.user)
    serialized = AuthorizedViewCourseSerializer(courses, many=True)
    return Response(serialized.data, status=200)


# Get all created courses
@swagger_auto_schema(method='GET', responses={200: InstructorViewCourseSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_created_courses(request):
    # check if the user is an instructor
    if request.user.role != "instructor":
        return Response({"message": "Unauthorized: You are not an instructor"}, status=401)
    
    courses = Course.objects.filter(instructor=request.user)
    serialized = InstructorViewCourseSerializer(courses, many=True)
    return Response(serialized.data, status=200)


# preview a course
@swagger_auto_schema(method='GET', responses={200: UnauthorizedViewCourseSerializer()})
@api_view(['GET'])
@permission_classes([AllowAny])
def preview_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        serialized = UnauthorizedViewCourseSerializer(course)
        return Response(serialized.data, status=200)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)
    

# Full view a course
@swagger_auto_schema(method='GET', responses={200: AuthorizedViewCourseSerializer()})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def full_view_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        if course not in request.user.enrolled_courses.all():
            return Response({"message": "Unauthorized: You are not enrolled in this course"}, status=401)
        serialized = AuthorizedViewCourseSerializer(course)
        return Response(serialized.data, status=200)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)
