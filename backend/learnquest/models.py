from django.db import models
from django.core.exceptions import ValidationError
import uuid
from utils.validators import YoutubeValidator


class Profile(models.Model):
    """
    Model representing a user profile.

    Fields:
        id (UUIDField): The unique identifier for the profile.
        user (OneToOneField): The user associated with the profile.
        profile_picture (ImageField): The profile picture of the user.
        bio (TextField): The bio or description of the user.
        twitter (URLField): The Twitter URL of the user.
        linkedIn (URLField): The LinkedIn URL of the user.
        location (CharField): The location of the user.
        phoneNumber (CharField): The phone number of the user.
        created_at (DateTimeField): The date and time when the profile was created.
        updated_at (DateTimeField): The date and time when the profile was last updated.

    """
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to = "profile_images/", default="default_profile.jpg", null = True, blank = True)
    bio = models.TextField(null =True, blank = True)
    twitter = models.URLField(null = True, blank = True)
    linkedIn = models.URLField(null =True, blank = True)
    location = models.CharField(max_length=200, blank=True, null = True)
    phoneNumber = models.CharField(max_length=20, blank=True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    

class Course(models.Model):
    """
    Model representing a course.

    Fields:
        id (UUIDField): The unique identifier for the course.
        title (CharField): The title of the course.
        instructor (ForeignKey): The instructor of the course.
        students (ManyToManyField): The students enrolled in the course.
        image (ImageField): The image of the course.
        price (FloatField): The price of the course.
        description (TextField): The description of the course.
        created_at (DateTimeField): The date and time when the course was created.
        updated_at (DateTimeField): The date and time when the course was last updated.

    """
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1024, blank=False, null=False)
    instructor = models.ForeignKey("authentication.User", on_delete = models.CASCADE, related_name = "presiding_courses", null = False, blank = False)
    students = models.ManyToManyField("authentication.User", related_name="enrolled_courses", through='CourseEnrollment')
    image = models.ImageField(upload_to="courses/", default= "default_course.jpg", null = True, blank = True)
    price = models.FloatField(default=0.00) 
    description = models.TextField(blank = True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def rating(self) -> float:
        """
        Calculate the rating of the course.

        Returns:
            float: The rating of the course.
        """
        ratings = [review.rating for review in self.reviews.all()]
        if len(ratings) == 0:
            return 0
        return sum(ratings) / len(ratings)
    
    
class CourseEnrollment(models.Model):
    """
    Model representing a course enrollment.

    Fields:
        course (ForeignKey): The course enrolled in.
        student (ForeignKey): The student enrolled in the course.

    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey("authentication.User", on_delete=models.CASCADE, null=True)
    
class Section(models.Model):
    """
    Model representing a section.

    Fields:
        id (UUIDField): The unique identifier for the section.
        title (CharField): The title of the section.
        course (ForeignKey): The course the section belongs to.
        created_at (DateTimeField): The date and time when the section was created.
        updated_at (DateTimeField): The date and time when the section was last updated.

    
    """
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1024, blank=False, null=False)
    course = models.ForeignKey(Course, related_name="sections", null = False, blank = False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def duration(self):
        """
        Calculate the duration of the section.

        Returns:
            int: The duration of the section (in seconds)
        """
        return sum([lesson.duration for lesson in self.lessons.all()])

class Lesson(models.Model):
    """
    Model representing a lesson.

    Fields:
        id (UUIDField): The unique identifier for the lesson.
        section (ForeignKey): The section the lesson belongs to.
        title (CharField): The title of the lesson.
        type (CharField): The type of the lesson (either "video" or "pdf").
        pdf (FileField): The PDF file of the lesson (required if type is "pdf").
        video_url (URLField): The URL of the video of the lesson (required if type is "video").
        summary (CharField): The summary of the lesson.
        created_at (DateTimeField): The date and time when the lesson was created.
        updated_at (DateTimeField): The date and time when the lesson was last updated.

    """
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    section = models.ForeignKey(Section, related_name="lessons", null = False, blank = False,on_delete=models.CASCADE)
    title = models.CharField(max_length=4096, blank=False, null=False)
    type = models.CharField(max_length=256, choices=[ ("link", "link"), ("pdf", "pdf")], default="link")
    pdf = models.FileField(upload_to='uploads/', null = True, blank = True)
    video_url = models.URLField(null = True, blank = True) 
    summary = models.TextField(null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    @property
    def duration(self) -> int:
        """
        Calculate the duration of the lesson.

        Returns:
            int: The duration of the lesson (in seconds)

        """
        if self.type == 'link':
            validator = YoutubeValidator(self.video_url)
            return validator.get_duration()
        return 0
    
    def save(self, *args, **kwargs):
        """
        Save the lesson.

        Raises:
            ValidationError: If the lesson type is "link" and the video URL is invalid.
            ValidationError: If the lesson type is "pdf" and the PDF file is not provided.

        """
        if self.type == 'link':
            validator = YoutubeValidator(self.video_url)
            if not validator.verify_link():
                raise ValidationError("Please provide a link from a supported domain. We support links from youtube")
        if (self.type == "link" and self.video_url is None) or (self.type == "pdf" and self.pdf is None):
            raise ValidationError("Provide either a link or upload a file")
        else:
            super().save(*args, **kwargs)
    

def validate_positive_choice(value):
    """
    Validate that the value is a positive choice.

    Args:
        value (int): The value to validate.

    Raises:
        ValidationError: If the value is not a positive choice.
    """
    choices = (1, 2, 3, 4, 5) 
    if value not in choices:
        raise ValidationError("Invalid choice for positive_field.")

class Review(models.Model):
    """
    Model representing a review.

    Fields:
        id (UUIDField): The unique identifier for the review.
        user (ForeignKey): The user who wrote the review.
        course (ForeignKey): The course the review is for.
        rating (PositiveIntegerField): The rating of the course (must be a positive choice).
        comment (TextField): The comment of the review.
        created_at (DateTimeField): The date and time when the review was created.
        updated_at (DateTimeField): The date and time when the review was last updated.

    """
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, null = False, blank = False, related_name="reviews")
    course =models.ForeignKey(Course, on_delete=models.CASCADE, null = False, blank = False, related_name="reviews")
    rating = models.PositiveIntegerField(null = False, blank = False, validators=[validate_positive_choice])
    comment = models.TextField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """
        Save the review.

        Raises:
            ValidationError: If the user is not enrolled in the course.

        """
        user= self.user
        enrolled_courses= user.enrolled_courses.all()
        if self.course not in enrolled_courses:
            raise ValidationError("User cannot review course that he is not enrolled in")
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ["user", "course"]
    
        
class InstructorApplication(models.Model):
    """
    Model representing an instructor application.

    Fields:
        id (UUIDField): The unique identifier for the instructor application.
        applicant (ForeignKey): The user who applied to be an instructor.
        reason (TextField): The reason why the user wants to be an instructor.
        status (CharField): The status of the application (either "pending", "declined", or "accepted").
        created_at (DateTimeField): The date and time when the application was created.
        updated_at (DateTimeField): The date and time when the application was last updated.

    """
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    application_statuses = [("pending", "pending"), ("declined", "declined"), ("accepted", "accepted")]
    applicant = models.ForeignKey("authentication.User", on_delete = models.CASCADE, related_name = "my_instructor_applications")
    reason = models.TextField(null = True, blank  = True)
    status = models.CharField(default= "pending", max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """
        Save the instructor application.

        Raises:
            ValidationError: If the user has a pending application or has already been accepted as an instructor.

        """
        applications = InstructorApplication.objects.filter(applicant = self.applicant)
        for application  in applications:
            if (application.status == "pending" and self.status != "accepted") or (application.status == "accepted" and self.status != "declined"):
                raise ValidationError("You have a pending application or you have already been accepted as an instructor.")
            if self.status == "accepted":
                user = self.applicant
                user.role = "instructor"
                user.save()
        if self.status == "declined":
            user = self.applicant
            user.role= "student"
            user.save()
        super().save(*args, **kwargs)
    


class Wallet(models.Model):
    """
    Model representing a wallet.

    Fields:
        id (UUIDField): The unique identifier for the wallet.
        balance (FloatField): The balance of the wallet.
        user (OneToOneField): The user associated with the wallet.
        currency (CharField): The currency of the wallet.
        created_at (DateTimeField): The date and time when the wallet was created.
        updated_at (DateTimeField): The date and time when the wallet was last updated.
    
    """
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    balance = models.FloatField(default = 0.00)
    user = models.OneToOneField("authentication.User", related_name = "wallet", on_delete=models.CASCADE)
    currency_choices = [("USD", "USD"), ("RUB", "RUB")]
    currency = models.CharField(default = "USD", max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Cart(models.Model):
    """
    Model representing a cart.

    Fields:
        id (UUIDField): The unique identifier for the cart.
        user (OneToOneField): The user associated with the cart.
        courses (ManyToManyField): The courses in the cart.
        created_at (DateTimeField): The date and time when the cart was created.
        updated_at (DateTimeField): The date and time when the cart was last updated.

    """
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    user = models.OneToOneField("authentication.User", related_name= "cart", on_delete = models.CASCADE, null = False, blank = False)
    courses = models.ManyToManyField(Course, related_name="carts", blank = True,through="CartCourse")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    @property
    def item_count(self):
        """
        Calculate the number of items in the cart.

        Returns:
            int: The number of items in the cart.
        """
        return self.courses.count()
    
    @property
    def total_price(self):
        """
        Calculate the total price of the cart.

        Returns:
            float: The total price of the cart.

        """
        course_prices = list(self.courses.values_list('price', flat=True))
        return sum(course_prices)


class CartCourse(models.Model):
    """
    Model representing a course in a cart.

    Fields:
        course (ForeignKey): The course in the cart.
        cart (ForeignKey): The cart the course is in.
        
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null = True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)