from django.urls import reverse, resolve 
from django.test import TestCase, Client
import random 
import string

from django.db import models
from authentication.models import * 
from django.contrib.auth import get_user_model
from learnquest.models import Profile, Lesson, Cart, Course, Section, InstructorApplication, Review, Wallet, CartCourse, CourseEnrollment

class TestCases(TestCase):
    def generate_email(self):
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        domain = ''.join(random.choices(string.ascii_lowercase, k=10))
        tlds = ['com', 'net', 'org', 'edu', 'gov']
        tld = random.choice(tlds)
        email = f"{username}@{domain}.{tld}"
        return email

    def generate_password(self):
        length = random.randint(1, 20)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return password

    def generate_random_text(self, length):
        characters = string.ascii_letters + string.digits + string.punctuation
        random_text = ''.join(random.choice(characters) for i in range(length))
        return random_text
    
    def setUp(self):
        self.User = get_user_model()
        self.client = Client()
        self.email = self.generate_email()
        self.password = self.generate_password() 

    def User_signup(self):
        url = reverse('signup')
        data = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(url, data)
        try: 
            self.assertEqual(response.status_code, 201)
            print("\033[92mUser signup successful\033[0m")
        except AssertionError:
            print("\033[91mUser signup failed\033[91m")

    def User_login(self):
        url = reverse('login')
        data = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(url, data)
        try:
            self.assertEqual(response.status_code, 200) 
            self.token = response.data['token']
            print(f"\033[92mUser login passed\033[0m")
        except AssertionError: 
            print(f"\033[91mUser login failed\033[91m")

    def Test_apply(self):
        self.User_signup()
        self.User_login()

        url = reverse('submit-instructor-application')
        data = {
            "reason": self.generate_random_text(20)
        }
        response = self.client.post(url, data, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Token {self.token}'})
        
        try: 
            self.assertEqual(response.status_code, 201)
            print("\033[92mApplication submission successful\033[0m")
        except AssertionError:
            print("\033[91mApplication submission failed\033[91m")

        # get the user object
        self.user = User.objects.get(email=self.email)

    def instructor_post_request(self, url, data):
        # make the user an instructor so the request is successful
        self.user.role = 'instructor'
        self.user.save()
        response = self.client.post(url, data, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Token {self.token}'})
        self.user.role = 'student'
        self.user.save()
        return response

    def instructor_delete_request(self, url):
        # make the user an instructor so the request is successful
        self.user.role = 'instructor'
        self.user.save()
        response = self.client.delete(url, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Token {self.token}'})
        self.user.role = 'student'
        self.user.save()
        return response


    def instructor_put_request(self, url, data):
        # make the user an instructor so the request is successful
        self.user.role = 'instructor'
        self.user.save()
        response = self.client.put(url, data, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Token {self.token}'})
        self.user.role = 'student'
        self.user.save()
        return response

    def Test_create_course(self):
        url = reverse('create-course')

        data = {
            "title": self.generate_random_text(10),
            "price": random.uniform(1.0, 50.0),
            "description": self.generate_random_text(20)
        }

        response = self.instructor_post_request(url, data)
        try: 
            self.assertEqual(response.status_code, 201)
            print("\033[92mCourse creation successful\033[0m")
        except AssertionError:
            print("\033[91mCourse creation failed\033[91m")

    def populate_courses(self):
        courses_count = random.randint(1, 5)
        print(f"populating db with {courses_count} more courses")

        for i in range(courses_count):
            print(f"adding {i+1}")
            self.Test_create_course()            

        print("\033[92mpopulation successful\033[0m")

    def Test_cart_add_and_get_cart(self):
        self.populate_courses()
        courses = Course.objects.all()

        price_sum = 0
        for i, course in enumerate(courses):
            price_sum += course.price 
            url = reverse('add-course-to-cart')
            data = {
                "course": course.id
            }
            response = self.client.post(url, data, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Token {self.token}'})
            try: 
                self.assertEqual(response.status_code, 201)
                print(f"\033[92madded course {i+1} to the cart\033[0m")
            except AssertionError:
                print(f"\033[91merror adding course {i+1} to the cart\033[91m")
            
        # Check that the number of course matches the number in get cart 
        url = reverse('get-cart')
        response = self.client.get(url, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Token {self.token}'})
        try: 
            self.assertEqual(response.data['item_count'], len(courses))
            print(f"\033[92mNumber of courses matches item count in the cart\033[0m")
        except AssertionError:
            print(f"\033[91mNumber of courses doesn't match item count in the cart\033[91m")  

        # Check that the price sum matches the total from get cart 
        url = reverse('get-cart')
        response = self.client.get(url, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Token {self.token}'})
        try: 
            self.assertAlmostEqual(response.data['total_price'], price_sum) # Due to precision issues
            print(f"\033[92mSum of prices matches the total in the cart\033[0m")
        except AssertionError:
            print(f"\033[91mSum of prices doesn't match the total in the cart\033[91m")  

    def Test_cart_remove_and_get_cart(self):
        courses = Course.objects.all()

        for i, course in enumerate(courses):
            temp = course.id
            url = reverse('delete-course-from-cart')
            data = {
                "course": course.id
            }
            response = self.client.delete(url, data, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Token {self.token}'})
            try: 
                self.assertEqual(response.status_code, 201)
                print(f"\033[92mDeleted course {i+1} from the cart\033[0m")
            except AssertionError:
                print(f"\033[91mError deleting course {i+1} from the cart\033[91m")
            
        # Check that the number of course in the cart is 0
        url = reverse('get-cart')
        response = self.client.get(url, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Token {self.token}'})
        try: 
            self.assertEqual(response.data['item_count'], 0)
            print(f"\033[92mNumber of courses in the cart 0\033[0m")
        except AssertionError:
            print(f"\033[91mNumber of courses in the cart is not 0\033[91m")  

        # Check that the price sum is 0 
        url = reverse('get-cart')
        response = self.client.get(url, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Token {self.token}'})
        try: 
            self.assertAlmostEqual(response.data['total_price'], float('0')) # Due to precision issues
            print(f"\033[92mSum of prices in the cart is 0\033[0m")
        except AssertionError:
            print(f"\033[91mSum of prices in the cart is not 0\033[91m")  

        # Try to delete a non existent course 
        print(temp)
        data = {
            "course": temp
        }
        url = reverse('delete-course-from-cart')
        response = self.client.delete(url, data, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Token {self.token}'})
        try: 
            self.assertEqual(response.status_code, 401)
            print(f"\n\033[92mCourse doesn't exist in cart\033[0m")
        except AssertionError:
            print(f"\n\033[91mError, course shouldn't exist\033[91m")

    def Test_delete_courses(self):
        courses = Course.objects.all()

        for i, course in enumerate(courses):
            url = reverse('delete-course', kwargs={'course_id': course.id})
            response = self.instructor_delete_request(url)
            try: 
                self.assertEqual(response.status_code, 200)
                print(f"\033[92mCourse {i+1} deleted successfully\033[0m")
            except AssertionError:
                print(f"\033[91mCourse {i+1} delete failed\033[91m")

        # Checking that all the courses are actually deleted 
        courses = Course.objects.all()
        try: 
            self.assertEqual(len(courses), 0)
            print(f"\n\033[92mAll courses deleted\033[0m")
        except AssertionError: 
            print(f"\n\033[91mAll courses not deleted\033[91m")

    def Test_create_course_section(self):
        self.populate_courses()
        courses = Course.objects.all()

        for i, course in enumerate(courses):
            url = reverse('create-section')
            data = {
                "title": self.generate_random_text(10),
                "course": course.id
            }
            response = self.instructor_post_request(url, data)
            try: 
                self.assertEqual(response.status_code, 201)
                print(f"\033[92mAdded a section to course {i+1}\033[0m")
            except AssertionError:
                print(f"\033[91mUnable to add a section to course {i+1}\033[91m")

    def Test_update_course_section(self):
        courses = Course.objects.all()

        for course in courses: 
            course_sections = Section.objects.filter(course=course)
            for section in course_sections:
                url = reverse('update-section')
                new_title = self.generate_random_text(10)
                data = {
                    "title": new_title,
                    "section": section.id
                }
                response = self.instructor_put_request(url, data)
                try: 
                    self.assertEqual(response.data['title'], new_title)
                    print(f"\033[92mUpdated section title for course {course}\033[0m")
                except AssertionError:
                    print(f"\033[91mUpdate section for course {course} failed\033[91m")

    def test_runner(self):
        self.Test_apply()
        self.Test_create_course()
        self.Test_cart_add_and_get_cart()
        self.Test_cart_remove_and_get_cart()
        self.Test_delete_courses()
        self.Test_create_course_section()
        self.Test_update_course_section()