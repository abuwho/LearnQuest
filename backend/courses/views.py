from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from courses.models import Course


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

# Get one course by id /course/<id>
@api_view(["GET"])
@permission_classes([AllowAny])
def get_course_by_id(request, id):
    data = request.data
    try:
        course = Course.objects.get(id=id)
        return Response({
            "course": course,
        }, status=200)
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
    
