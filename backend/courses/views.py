from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from courses.models import Course, Category, Lesson, Review
from .serializer import CourseSerializer, ReviewSerializer
from rest_framework import status

# Get all courses
@api_view(["GET"])
@permission_classes([AllowAny])
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
    
# Get all courses by category /courses/<category>
@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_courses_by_category(request, category):
    data = request.data
    try:
        courses = Course.objects.filter(category=category)
        return Response({
            "courses": courses,
        }, status=200)
    except Exception as e:
        return Response(
            {}, status=400
        )


# Get one course by id /course/<id>
@swagger_auto_schema(methods=['GET'], 
                     responses={200: CourseSerializer(), 400: {}})
@api_view(["GET"])
@permission_classes([AllowAny])
def get_course_by_id(request, id):
    if request.method=='GET':
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
@permission_classes([AllowAny])
def get_lessons_by_course_id(request, id):
    data = request.data
    try:
        course = Course.objects.get(id=id)
        lessons = course.lessons.all()
        return Response({
            "lessons": lessons,
        }, status=200)
    except Exception as e:
        return Response(
            {}, status=400
        )


# Get lesson by id /course/<id>/lessons/<id>
@api_view(["GET"])
@permission_classes([AllowAny])
def get_lesson_by_id(request, id, lesson_id):
    data = request.data
    try:
        lesson = Lesson.objects.get(id=lesson_id)
        return Response({
            "lesson": lesson,
        }, status=200)
    except Exception as e:
        return Response(
            {}, status=400
        )
    

# Get all reviews in a course /course/<id>/reviews
@api_view(["GET"])
@permission_classes([AllowAny])
def get_reviews_by_course_id(request, id):
    reviews = Review.objects.filter(course__id=id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

# Get review by id /course/<id>/reviews/<id>
@api_view(["GET"])
@permission_classes([AllowAny])
def get_review_by_id(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, course__id=id)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)


# Get courses that a user has enrolled in only if they are authenticated /courses/my
@api_view(["GET"])
@permission_classes([AllowAny])
def get_courses_by_user(request):
    data = request.data
    try:
        courses = Course.objects.filter(user=request.user)
        return Response({
            "courses": courses,
        }, status=200)
    except Exception as e:
        return Response(
            {}, status=400
        )

@swagger_auto_schema(methods=['GET'],
                     responses={200: CourseSerializer(), 400: {}})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_courses(request):
    if request.method=='GET':
        try:
            courses = Course.objects.filter(user=request.user)
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {}, status=status.HTTP_400_BAD_REQUEST
            )

# Post a course if the user is an instructor /courses
@swagger_auto_schema(methods=["POST","PUT","DELETE"], request_body=CourseSerializer,
                     responses={201: CourseSerializer(), 400: {},403: "Forbidden",})
@api_view(["POST","PUT","DELETE"])
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

@swagger_auto_schema(methods=["GET"],
                     responses={201: CourseSerializer(), 400: {},403: "Forbidden",})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_courses(request):

    if request.method == "GET":
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    else:
        return Response({"message": "Invalid request method."}, status=405)