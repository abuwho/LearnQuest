from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from courses.models import Course, Category, Lesson, Review
from .serializer import CourseSerializer, ReviewSerializer, LessonSerializer, DisplayLessonSerializer
from rest_framework import status


# Create, update, delete a course
@swagger_auto_schema(methods=["POST", "PUT", "DELETE"], request_body=CourseSerializer,
                     responses={201: CourseSerializer(), 400: {}, 403: "Forbidden", })
@api_view(["POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def CRUD_courses(request):
    if request.method == "POST":
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the user is an instructor
            if request.user.role == "instructor":
                serializer.save(instructor=request.user)
                return Response(serializer.data, status=201)
            else:
                return Response({"message": "Only instructors can create courses."}, status=403)
        return Response(serializer.errors, status=400)

    elif request.method == "PUT" or request.method == "DELETE":
        course = get_object_or_404(Course, id=request.data.get("id"))

        # Check if the user is an instructor and the owner of the course
        if not request.user.role == "instructor" or course.instructor != request.user:
            return Response({"message": "You don't have permission to perform this action."}, status=403)

        if request.method == "PUT":
            serializer = CourseSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

        elif request.method == "DELETE":
            course.delete()
            return Response({"message": "Course deleted successfully."}, status=204)

    return Response({"message": "Invalid request method."}, status=405)


# Get all courses
@swagger_auto_schema(methods=["GET"],
                     responses={201: CourseSerializer(), 400: {}, 403: "Forbidden", })
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_courses(request):

    if request.method == "GET":
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    else:
        return Response({"message": "Invalid request method."}, status=405)



@swagger_auto_schema(methods=['GET'],
                     responses={200: CourseSerializer(), 400: {}})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_courses(request):
    if request.method == 'GET':
        try:
            courses = Course.objects.filter(user=request.user)
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {}, status=status.HTTP_400_BAD_REQUEST
            )


# /courses/<category>
@swagger_auto_schema(methods=['GET'],
                     responses={200: CourseSerializer(many=True), 400: {}})
@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_courses_by_category(request, category):
    """
    Retrieve all courses belonging to a specific category.

    :param request: The HTTP request object.
    :param category: The category name to filter the courses.
    :return: A response containing the courses in the specified category.
    :rtype: Response

    Exceptions:

        400 Bad Request: If there is an error processing the request.

    Swagger Documentation:

        HTTP Method: GET
        Response:
            200 OK: CourseSerializer(many=True) - A successful response with a list of courses.
            400 Bad Request: An error response when there is an issue with the request.
    """
    data = request.data
    try:
        courses = Course.objects.filter(category__name=category)
        serializer = CourseSerializer(data=courses, many=True)
        return Response({
            "courses": serializer.data,
        }, status=200)
    except Exception as e:
        return Response(
            {}, status=400
        )


# /courses/<id>
@swagger_auto_schema(methods=['GET'],
                     responses={200: CourseSerializer(), 400: {}})
@api_view(["GET"])
@permission_classes([AllowAny])
def get_course_by_id(request, id):
    if request.method == 'GET':
        try:
            course = Course.objects.get(id=id)
            serializer = CourseSerializer(course, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {}, status=400
            )


# Get all lessons in a course /course/<id>/lessons
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_lessons_by_course_id(request, id):
    if request.method == 'GET':
        try:
            course = get_object_or_404(Course, id=request.data.get("id"))
            if request.user in course.students:
                lessons = Lesson.objects.filter(course__id=id)
                serializer = DisplayLessonSerializer(lessons, many=True)
                return Response(serializer.data)
            else:
                return Response({}, status=401)
        except Exception as e:
            return Response(
                {}, status=400
            )
    return Response({"message": "Invalid request method."}, status=405)



# Create, update, delete a lesson
@swagger_auto_schema(methods=["POST", "PUT", "DELETE"], request_body=LessonSerializer,
                     responses={201: LessonSerializer(), 400: {}, 403: "Forbidden", })
@api_view(["POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def CRUD_lesson(request):
    """
    Create, update, or delete a lesson.
    @param request: The HTTP request object.
    @return: The HTTP response object with the appropriate status and data.
    """
    if request.method == "POST":
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            course_id = serializer.validated_data.get("course")
            course = get_object_or_404(Course, id=course_id)

            # Check if the user is the instructor of the associated course
            if course.instructor != request.user:
                return Response({"message": "You don't have permission to create a lesson for this course."}, status=403)

            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == "PUT" or request.method == "DELETE":
        lesson_id = request.data.get("id")
        lesson = get_object_or_404(Lesson, id=lesson_id)
        course = lesson.course

        # Check if the user is the instructor of the associated course
        if course.instructor != request.user:
            return Response({"message": "You don't have permission to perform this action."}, status=403)

        if request.method == "PUT":
            serializer = LessonSerializer(lesson, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

        elif request.method == "DELETE":
            lesson.delete()
            return Response({"message": "Lesson deleted successfully."}, status=204)

    return Response({"message": "Invalid request method."}, status=405)



# Create, update, delete a review
@swagger_auto_schema(methods=["POST", "PUT", "DELETE"], request_body=ReviewSerializer,
                        responses={201: ReviewSerializer(), 400: {}, 403: "Forbidden", })
@api_view(["POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def CRUD_review(request):
    if request.method == "POST":
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            course_id = serializer.validated_data.get("course")
            course = get_object_or_404(Course, id=course_id)

            # Check if the user is a student
            if request.user.role == "student":
                serializer.save(user=request.user)
                return Response(serializer.data, status=201)
            else:
                return Response({"message": "Only students can create reviews."}, status=403)
        return Response(serializer.errors, status=400)

    elif request.method == "PUT" or request.method == "DELETE":
        review_id = request.data.get("id")
        review = get_object_or_404(Review, id=review_id)
        course = review.course

        # Check if the user is a student and the owner of the review
        if not request.user.role == "student" or review.user != request.user:
            return Response({"message": "You don't have permission to perform this action."}, status=403)

        if request.method == "PUT":
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)

        elif request.method == "DELETE":
            review.delete()
            return Response({"message": "Review deleted successfully."}, status=204)

    return Response({"message": "Invalid request method."}, status=405)


# Get all reviews for a course /course/<id>/reviews/all
@api_view(["GET"])
@permission_classes([AllowAny])
def get_reviews_by_course_id(request, id):
    reviews = Review.objects.filter(course=id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)
