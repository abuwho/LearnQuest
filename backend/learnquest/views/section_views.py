from .views_imports import *

@swagger_auto_schema(methods=['POST'], request_body=RequestCreateSectionSerializer,
                     responses={201: ResponseCreateSectionSerializer(), 400: {}})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_section(request):
    data = request.data
    serialized = RequestCreateSectionSerializer(data= data)
    try:
        serialized.is_valid(raise_exception=True)

        user = request.user
        title = serialized.data.get("title")
        course = serialized.data.get("course")

        course_object = Course.objects.get(id=course)

        if user != course_object.instructor:
            raise ValueError("The current user cannot add a section for this course")
        
        course_sections = Section.objects.filter(course=course)

        for section in course_sections: 
            if section.title == title: 
                raise ValueError("This course already contains the provided section title")

        created_section = Section.objects.create(title=title, course=course_object)
        created_section.save()

        return Response(ResponseCreateSectionSerializer(created_section).data, status= 201)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)

@swagger_auto_schema(methods=['PUT'], request_body=RequestUpdateSectionSerializer,
                     responses={200: ResponseUpdateSectionSerializer(), 400: {}})
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_section(request):
    data = request.data
    serialized = RequestUpdateSectionSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)

        user = request.user
        title = serialized.data.get("title")

        section = serialized.data.get("section")

        section_object = Section.objects.get(id=section)

        if user != section_object.course.instructor:
            raise ValueError("The current user cannot update the section title")

        if title is not None:    
            section_object.title = title
            section_object.save()

        return Response(ResponseUpdateSectionSerializer(section_object).data, status=200)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)


@swagger_auto_schema(methods=['POST'], request_body=RequestDeleteSectionSerializer,
                     responses={200: {}, 400: {}})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_section(request):
    data = request.data
    serialized = RequestDeleteSectionSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)

        user = request.user
        section = serialized.data.get("section")

        section_object = Section.objects.get(id=section)

        if user != section_object.course.instructor:
            raise ValueError("The current user cannot delete this section")

        section_object.delete()

        return Response({}, 200)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)


# Get all lessons in a section
@swagger_auto_schema(method='GET', responses={200: EnrolledViewSectionSerializer(many=True)})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_lessons_in_section(request, section_id):
    try:
        section = Section.objects.get(id=section_id)
        course = section.course
        if course.instructor != request.user and request.user not in course.students.all():
            return Response({"message": "Unauthorized: You are not enrolled in the course"}, status=401)
        lessons = section.lessons
        serialized = EnrolledViewSectionSerializer(section)
        print(serialized)
        return Response(serialized.data, status=200)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)
