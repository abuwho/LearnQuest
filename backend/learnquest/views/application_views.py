from .views_imports import *


@swagger_auto_schema(methods=['POST'], request_body=RequestInstructorApplicationSerializer,
                     responses={201: ResponseInstructorApplicationSerializer(), 400: {}})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_instructor_application(request):
    """
    Submit an instructor application.

    This endpoint is used to submit an instructor application.

    Args:
        request (Request): The request object.
    
    Returns:
        Response: The response object.
    """
    data = request.data
    serialized = RequestInstructorApplicationSerializer(data= data)
    try:
        serialized.is_valid(raise_exception=True)
        applicant = request.user
        application = InstructorApplication(applicant = applicant, reason = serialized.validated_data.get("reason"))
        application.save()
        return Response(ResponseInstructorApplicationSerializer(application).data, status= 201)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status= 400)