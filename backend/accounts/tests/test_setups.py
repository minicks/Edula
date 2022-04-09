import json

from django.urls import reverse
from rest_framework.test import APITestCase

from schools.models import School
from ..models import User, Student, Teacher

# Create your tests here.
class TestSetUp(APITestCase):
    """ Test set up class
    test set up test data for accounts app
    """
    @classmethod
    def setUpTestData(cls):
        # basic informations
        cls.jwt_url = reverse('JWT_login')
        cls.content_type = 'application/json'

        # data
        cls.student_info = {
            'username': 'student',
            'email': 'example@string.com',
            'password': 'student',
            'status': 'ST',
        }
        cls.teacher_info = {
            'username': 'teacher',
            'email': 'example@string.com',
            'password': 'teacher',
            'status': 'TE',
        }
        cls.school_admin_info = {
            'username': 'school_admin',
            'email': 'example@string.com',
            'password': 'school_admin',
            'status': 'SA',
        }
        cls.school_data ={
            'name': 'ssafy',
            'abbreviation': 'ss',
        }

        # json data
        cls.student_info_json = json.dumps(cls.student_info)
        cls.teacher_info_json = json.dumps(cls.teacher_info)
        cls.school_admin_info_json = json.dumps(cls.school_admin_info)

        # object
        cls.school = School.objects.create(
            name=cls.school_data['name'],
            abbreviation=cls.school_data
        )
        cls.user_student = User.objects.create_user(
            username=cls.student_info['username'],
            email=cls.student_info['email'],
            password=cls.student_info['password'],
            status=cls.student_info['status'],
        )
        cls.user_teacher = User.objects.create_user(
            username=cls.teacher_info['username'],
            email=cls.teacher_info['email'],
            password=cls.teacher_info['password'],
            status=cls.teacher_info['status'],
        )
        cls.user_school_admin = User.objects.create_user(
            username=cls.school_admin_info['username'],
            email=cls.school_admin_info['email'],
            password=cls.school_admin_info['password'],
            status=cls.school_admin_info['status'],
        )
        cls.student_student = Student.objects.create(
            user=cls.user_student,
            school=cls.school,
        )
        cls.teacher_teacher = Teacher.objects.create(
            user=cls.user_teacher,
            school=cls.school,
        )
