from .views_imports import *


@swagger_auto_schema(methods=['POST'], request_body=AddToCartSerializer,
                     responses={201: DisplayCartSerializer(), 400: {}})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_course_to_cart(request):
    data = request.data
    serialized = AddToCartSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        courseID = serialized.data.get('course')
        course_object = Course.objects.get(id=courseID)
        user = request.user
        cart = Cart.objects.get(user=user)

        # Check if the user already has this course in the cart
        if CartCourse.objects.filter(cart=cart, course=course_object).exists():
            raise ValueError("This course is in the cart already")

        # Check if the user is already enrolled in this course 
        if course_object in request.user.enrolled_courses.all(): 
            raise ValueError("Can't add an enrolled course to the cart")   

        buy = CartCourse.objects.create(course=course_object, cart=cart)
        buy.save()
        return Response(DisplayCartSerializer(cart).data, 201)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)


@swagger_auto_schema(methods=['GET'],
                     responses={201: DisplayCartSerializer(), 400: {}})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):
    try:
        user = request.user 
        cart = Cart.objects.get(user=user)
        serializer = DisplayCartSerializer(cart)
        return Response(serializer.data, status=201)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)


@swagger_auto_schema(methods=['DELETE'], request_body=RemoveFromCartSerializer,
                     responses={201: DisplayCartSerializer(), 400: {}})
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_course_from_cart(request):
    data = request.data
    serialized = RemoveFromCartSerializer(data=data)
    try:
        serialized.is_valid(raise_exception=True)
        courseID = serialized.data.get('course')
        course_object = Course.objects.get(id=courseID)
        user = request.user
        cart = Cart.objects.get(user=user)

        # Check if the user has this course in the cart
        if CartCourse.objects.filter(cart=cart, course=course_object).exists():
            cart_course_object = CartCourse.objects.get(cart=cart, course=course_object)
            cart_course_object.delete()

        return Response(DisplayCartSerializer(cart).data, 201)
    except Exception as e:
        return Response({"message": "Invalid Request", "error": str(e)}, status=400)
    
@swagger_auto_schema(methods=['POST'],
                     responses={201: DisplayCartSerializer(), 400: {}, 500 : {}})
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkout(request):
    try:
        user = request.user
        cart = user.cart
        wallet = user.wallet

        if wallet.balance < cart.total_price:
            return Response({"message":"Insufficient Fund"}, status= 401)

        cartcourses = CartCourse.objects.filter(cart = cart).all()
        for cartcourse in cartcourses:
            CourseEnrollment.objects.create(student= user, course = cartcourse.course)
            wallet.balance -= cartcourse.course.price
            cartcourse.delete()
        wallet.save()
        return Response(DisplayCartSerializer(cart).data, 201)
    except Exception as e:
        return Response({"message": "Something went wrong", "error": str(e)}, status=500)