from .views_imports import *

# Create a lesson
@swagger_auto_schema(method='POST', request_body=RequestCreateLessonSerializer, responses={201: ResponseCreateLessonSerializer()})
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def create_lesson(request):
    data = request.data
    serialized = RequestCreateLessonSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        section = Section.objects.get(id=serialized.data.get("section"))
        course = section.course

        if course.instructor != request.user:
            return Response({"message": "Unauthorized: You are not the instructor of this course"}, status=401)
        
        lesson = Lesson(title=serialized.validated_data.get("title"), section=section,
                        type=serialized.validated_data.get("type"), pdf=serialized.validated_data.get("pdf"),
                        video_url=serialized.validated_data.get("video_url"))
        lesson.save()
        return Response(ResponseCreateLessonSerializer(lesson).data, status=201)
    
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)


# Update a lesson
@swagger_auto_schema(method='PUT', request_body=RequestUpdateLessonSerializer, responses={200: ResponseUpdateLessonSerializer()})
@api_view(['PUT'])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def update_lesson(request):
    data = request.data
    serialized = RequestUpdateLessonSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        lesson = Lesson.objects.get(id=serialized.validated_data.get("id"))
        section = Section.objects.get(id=serialized.validated_data.get("section"))
        course = section.course
        if course.instructor != request.user:
            return Response({"message": "Unauthorized: You are not the instructor of this course"}, status=401)
        
        # Update the lesson
        if serialized.validated_data.get("title") is not None:
            lesson.title = serialized.validated_data.get("title")
        if serialized.validated_data.get("type") is not None:
            lesson.type = serialized.validated_data.get("type")
        if serialized.validated_data.get("pdf") is not None:
            lesson.pdf = serialized.validated_data.get("pdf")
        if serialized.validated_data.get("video_url") is not None:
            lesson.video_url = serialized.validated_data.get("video_url")
        lesson.save()
        return Response(ResponseUpdateLessonSerializer(lesson).data, status=200)

    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)


# Delete a lesson
@swagger_auto_schema(method='DELETE', responses={200: {}})
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_lesson(request, lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
        section = lesson.section
        course = section.course
        if course.instructor != request.user:
            return Response({"message": "Unauthorized: You are not the instructor of this course"}, status=401)
        lesson.delete()
        return Response({}, status=200)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)


