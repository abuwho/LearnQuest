from django.db import models
from django.core.exceptions import ValidationError
import uuid
from utils.validators import YoutubeValidator


class Profile(models.Model):
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
        ratings = [review.rating for review in self.reviews.all()]
        if len(ratings) == 0:
            return 0
        return sum(ratings) / len(ratings)
    
    
class CourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey("authentication.User", on_delete=models.CASCADE, null=True)
    
class Section(models.Model):
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1024, blank=False, null=False)
    course = models.ForeignKey(Course, related_name="sections", null = False, blank = False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def duration(self):
        return sum([lesson.duration for lesson in self.lessons.all()])

class Lesson(models.Model):
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    section = models.ForeignKey(Section, related_name="lessons", null = False, blank = False,on_delete=models.CASCADE)
    title = models.CharField(max_length=4096, blank=False, null=False)
    type = models.CharField(max_length=256, choices=[ ("link", "link"), ("pdf", "pdf")], default="link")
    pdf = models.FileField(upload_to='uploads/', null = True, blank = True)
    video_url = models.URLField(null = True, blank = True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    @property
    def duration(self) -> int:
        if self.type == 'link':
            validator = YoutubeValidator(self.video_url)
            return validator.get_duration()
        return 0
    
    def save(self, *args, **kwargs):
        if self.type == 'link':
            validator = YoutubeValidator(self.video_url)
            if not validator.verify_link():
                raise ValidationError("Please provide a link from a supported domain. We support links from youtube")
        if (self.type == "link" and self.video_url is None) or (self.type == "pdf" and self.pdf is None):
            raise ValidationError("Provide either a link or upload a file")
        else:
            super().save(*args, **kwargs)
    

def validate_positive_choice(value):
    choices = (1, 2, 3, 4, 5) 
    if value not in choices:
        raise ValidationError("Invalid choice for positive_field.")

class Review(models.Model):
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    user = models.ForeignKey("authentication.User", on_delete=models.CASCADE, null = False, blank = False, related_name="reviews")
    course =models.ForeignKey(Course, on_delete=models.CASCADE, null = False, blank = False, related_name="reviews")
    rating = models.PositiveIntegerField(null = False, blank = False, validators=[validate_positive_choice])
    comment = models.TextField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        user= self.user
        enrolled_courses= user.enrolled_courses.all()
        if self.course not in enrolled_courses:
            raise ValidationError("User cannot review course that he is not enrolled in")
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ["user", "course"]
    
        
class InstructorApplication(models.Model):
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    application_statuses = [("pending", "pending"), ("declined", "declined"), ("accepted", "accepted")]
    applicant = models.ForeignKey("authentication.User", on_delete = models.CASCADE, related_name = "my_instructor_applications")
    reason = models.TextField(null = True, blank  = True)
    status = models.CharField(default= "pending", max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
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
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    balance = models.FloatField(default = 0.00)
    user = models.OneToOneField("authentication.User", related_name = "wallet", on_delete=models.CASCADE)
    currency_choices = [("USD", "USD"), ("RUB", "RUB")]
    currency = models.CharField(default = "USD", max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Cart(models.Model):
    id = models.UUIDField(unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    user = models.OneToOneField("authentication.User", related_name= "cart", on_delete = models.CASCADE, null = False, blank = False)
    courses = models.ManyToManyField(Course, related_name="carts", blank = True,through="CartCourse")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    @property
    def item_count(self):
        return len(self.courses)
    
    @property
    def total_price(self):
        return sum([course.price for course in self.courses.all()])


class CartCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null = True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)