from .views_imports import *


# Get all courses
@swagger_auto_schema(method='GET', responses={200: UnauthorizedViewCourseSerializer(many=True)})
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_courses(request):
    """
    Get all courses.

    This endpoint is used to get all the courses.

    Args:
        request (Request): The request object.
    
    Returns:
        Response: The response object.
    """
    courses = Course.objects.all()
    serialized = UnauthorizedViewCourseSerializer(courses, many=True)
    return Response(serialized.data, status=200)



# Create a course
@swagger_auto_schema(method='POST', request_body=RequestCreateCourseSerializer, responses={201: ResponseCreateCourseSerializer()})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_course(request):
    """
    Create a course.

    This endpoint is used to create a course. The user must be an instructor.

    Args:
        request (Request): The request object.

    Returns:
        Response: The response object.
    """
    data = request.data
    print(data, type(data))
    serialized = RequestCreateCourseSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        if (request.user.role != "instructor"):
            return Response({"message": "Unauthorized: You are not an instructor"}, status=401)
        course = Course(title=serialized.validated_data.get("title"), instructor=request.user,
                        price=serialized.validated_data.get("price"),
                        description=serialized.validated_data.get("description"),
                        image=serialized.validated_data.get("image") if serialized.validated_data.get("image") else "default_course.jpg")
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
    """
    Update a course.

    This endpoint is used to update a course. The user must be the instructor of the course.

    Parameters:
        request (HttpRequest): The HTTP request object.
        course_id (int): The ID of the course to update.

    Returns:
        Response: The response containing the updated course data.

    """
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
    """
    Delete a course.

    This endpoint is used to delete a course. The user must be the instructor of the course.

    Parameters:
        request (HttpRequest): The HTTP request object.
        course_id (int): The ID of the course to delete.

    Returns:
        Response: The response indicating the success or failure of the deletion.

    """
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
    """
    Get all enrolled courses.

    This endpoint is used to get all the courses enrolled by the current user.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The response containing the serialized enrolled courses.

    """
    courses = Course.objects.filter(students=request.user)
    serialized = AuthorizedViewCourseSerializer(courses, many=True)
    return Response(serialized.data, status=200)


# Get all created courses
@swagger_auto_schema(method='GET', responses={200: InstructorViewCourseSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_created_courses(request):
    """
    Get all created courses.

    This endpoint is used to get all the courses created by the current user. The user must be an instructor.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The response containing the serialized created courses.

    """
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
    """
    Preview a course.

    This endpoint is used to get the preview of a course. The user does not need to be enrolled in the course or be the instructor of the course.

    Parameters:
        request (HttpRequest): The HTTP request object. (NOT used, because preview is allowed for all users)
        course_id (int): The ID of the course to preview.

    Returns:
        Response: The response containing the serialized course for preview.

    """
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
    """
    Full view of a course.

    This endpoint is used to get the full view of a course. The user must be enrolled in the course or be the instructor of the course.

    Parameters:
        request (HttpRequest): The HTTP request object.
        course_id (int): The ID of the course to view.

    Returns:
        Response: The response containing the serialized course for full view.

    """
    try:
        course = Course.objects.get(id=course_id)
        if course not in request.user.enrolled_courses.all() and request.user != course.instructor:
            return Response({"message": "Unauthorized: You are not enrolled in this course"}, status=401)
        serialized = AuthorizedViewCourseSerializer(course)
        return Response(serialized.data, status=200)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)
