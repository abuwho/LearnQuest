from .serializers_import import *
from .section_serializers import EnrolledViewSectionSerializer, UnenrolledViewSectionSerializer
from .review_serializers import ViewReviewSerializer
from authentication.serializer import DisplayUserSerializer


class CartDisplayCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying course details in the cart.

    Fields:
        instructor (SerializerMethodField): The instructor of the course (read-only).

    Meta:
        model (Course): The Course model to serialize.
        fields (list): List of fields to include in the serialization.

    """
    instructor = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Course
        fields = ["id", "title", "instructor", "image", "price", "description", "created_at", "updated_at"]
        
    def get_instructor(self, instance):
        return DisplayUserSerializer(instance= instance.instructor).data


class UnauthorizedViewCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying unauthorized course details.

    Fields:
        rating (SerializerMethodField): The rating of the course (read-only).
        sections (SerializerMethodField): The sections of the course (read-only).

    Meta:
        model (Course): The Course model to serialize.
        fields (list): List of fields to include in the serialization.

    """
    rating = serializers.SerializerMethodField(read_only = True)
    sections= serializers.SerializerMethodField(read_only = True)
    
    class Meta:
        model = Course
        fields = ["id", "rating", "title", "instructor", "image", "price", "description", "created_at", "updated_at", "sections"]
        
    def get_rating(self, instance):
        return instance.rating
    
    def get_sections(self, instance):
        return UnenrolledViewSectionSerializer(instance= instance.sections, many = True).data
    


class AuthorizedViewCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying authorized course details.

    Fields:
        rating (SerializerMethodField): The rating of the course (read-only).
        sections (SerializerMethodField): The sections of the course (read-only).
        reviews (SerializerMethodField): The reviews of the course (read-only).

    Meta:
        model (Course): The Course model to serialize.
        fields (list): List of fields to include in the serialization.

    """
    rating = serializers.SerializerMethodField(read_only = True)
    sections = serializers.SerializerMethodField(read_only = True)
    reviews = serializers.SerializerMethodField(read_only  = True)
    class Meta:
        model = Course
        fields = ["id", "rating", "title", "instructor", "image", "price", "reviews","description", "created_at", "updated_at", "sections"]
        
    def get_rating(self, instance):
        return instance.rating
    
    def get_sections(self, instance):
        return EnrolledViewSectionSerializer(instance= instance.sections, many = True).data
    

    def get_reviews(self, instance):
        return ViewReviewSerializer(instance= instance.reviews, many = True).data
    
    
    
    
class InstructorViewCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying instructor course details.

    Fields:
        students (SerializerMethodField): The students enrolled in the course (read-only).
        rating (SerializerMethodField): The rating of the course (read-only).

    Meta:
        model (Course): The Course model to serialize.
        fields (list): List of fields to include in the serialization.

    """
    students = serializers.SerializerMethodField(read_only = True)
    rating = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Course
        fields = ["id","rating", "title", "instructor", "students", "image", "price", "description", "created_at", "updated_at", "sections"]
        
    def get_students(self, instance):
        return DisplayUserSerializer(instance= instance.students, many = True).data
    
    def get_rating(self, instance):
        return instance.rating
    

    
class RequestCreateCourseSerializer(serializers.Serializer):
    """
    Serializer for creating a course.

    Fields:
        title (CharField): The title of the course.
        price (FloatField): The price of the course (optional).
        description (CharField): The description of the course (optional).
        image (ImageField): The image of the course (optional).

    """
    title = serializers.CharField()
    price = serializers.FloatField(required = False)
    description =  serializers.CharField(allow_null=True, required= False)
    image = serializers.ImageField(required= False)


class ResponseCreateCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the response of creating a course.

    Fields:
        rating (SerializerMethodField): The rating of the course (read-only).

    Meta:
        model (Course): The Course model to serialize.
        fields (list): List of fields to include in the serialization.

    """
    rating = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Course
        fields = ["id","rating", "title", "instructor", "students", "image", "price", "description", "created_at", "updated_at"]
        
    def get_rating(self, instance):
        return instance.rating


    
class RequestUpdateCourseSerializer(serializers.Serializer):
    """
    Serializer for updating a course.

    Fields:
        title (CharField): The updated title of the course (optional).
        price (FloatField): The updated price of the course (optional).
        description (CharField): The updated description of the course (optional).
        image (ImageField): The updated image of the course (optional).

    """
    title = serializers.CharField(allow_null=True, required= False)
    price = serializers.FloatField(required= False)
    description =  serializers.CharField(allow_null=True, required= False)
    image = serializers.ImageField(required= False)
    

class ResponseUpdateCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the response of updating a course.

    Fields:
        rating (SerializerMethodField): The rating of the course (read-only).

    Meta:
        model (Course): The Course model to serialize.
        fields (list): List of fields to include in the serialization.

    """
    rating = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Course
        fields = ["id", "rating", "title", "instructor", "students", "image", "price", "description", "created_at", "updated_at"]
        
    def get_rating(self, instance):
        return instance.rating
