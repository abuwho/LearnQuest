from .views_imports import *

@swagger_auto_schema(methods=['GET'], responses={200: ViewReviewSerializer(many=True), 400: {}})
@api_view(["GET"])
@permission_classes([AllowAny])
def get_reviews(request, course_id):
    """
    Get all reviews in a course.

    This endpoint is used to get all reviews in a course.

    Parameters:
        request (HttpRequest): The HTTP request object.
        course_id (int): The id of the course.

    """
    try:
        course = Course.objects.get(id=course_id)
        reviews = course.reviews.all()
        serialized = ViewReviewSerializer(reviews, many=True)
        return Response(serialized.data, status=200)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)
    


@swagger_auto_schema(methods=['POST'], request_body=RequestCreateReviewSerializer,
                        responses={201: ResponseCreateReviewSerializer(), 400: {}})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request):
    """
    Create a review.

    This endpoint is used to create a review. The user must be enrolled in the course. The user cannot be the instructor of the course. The user cannot review a course more than once.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The response containing the serialized created review.

    """
    data = request.data
    serialized = RequestCreateReviewSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        user = request.user
        course = serialized.data.get("course")
        rating = serialized.data.get("rating")
        comment = serialized.data.get("comment")
        course_object = Course.objects.get(id=course)

        # Check if user is the instructor of the course
        if course_object.instructor == user:
            return Response({"message": "Unauthorized: You are the instructor of this course, so, you cannot review it"}, status=401)
        
        enrolled_courses = user.enrolled_courses.all()
        if course_object not in enrolled_courses:
            return Response({"message": "Unauthorized: You are not enrolled in this course"}, status=401)
        
        reviews = Review.objects.filter(user=user, course=course_object)
        if reviews.exists():
            return Response({"message": "Unauthorized: You have already reviewed this course"}, status=401)
        
        review = Review.objects.create(user=user, course=course_object, rating=rating, comment=comment)
        serialized = ResponseCreateReviewSerializer(review)
        return Response(serialized.data, status=201)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)
        
    

