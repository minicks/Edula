"""Test Set up for School App
"""
import json

from django.urls import reverse
from django.contrib.auth.hashers import make_password
import factory
from rest_framework.test import APITestCase


class UserFactory(factory.django.DjangoModelFactory):
    """Usser Factory
    """
    class Meta:
        model = 'accounts.User'

    username= factory.Sequence(lambda n: f'user{n}')
    email = factory.Faker('email')
    password = factory.LazyFunction(lambda: make_password('test1234!'))
    first_name = factory.Faker('name', locale='ko_KR')


class SchoolFactory(factory.django.DjangoModelFactory):
    """School Factory
    """
    class Meta:
        model = 'schools.School'

    name = factory.Faker('company')
    abbreviation = factory.Sequence(lambda n: f'abb{n}')


class LectureFactory(factory.django.DjangoModelFactory):
    """Lecture Factory
    """
    class Meta:
        model = 'schools.Lecture'

    name = factory.Faker('job')
    time_list = {'test': 'test'}


class ClassroomFactory(factory.django.DjangoModelFactory):
    """Classrooom Factory
    """
    class Meta:
        model = 'schools.Classroom'

    class_grade = factory.LazyFunction(lambda: 1)
    class_num = factory.Sequence(lambda n: int(n))
    school = factory.SubFactory(SchoolFactory)


class UserStudentFactory(UserFactory):
    """User Student Factory
    """
    class Meta:
        model = 'accounts.User'

    status = 'ST'


class StudentFactory(factory.django.DjangoModelFactory):
    """Student Factory
    """
    class Meta:
        model = 'accounts.Student'

    user = factory.SubFactory(UserStudentFactory)


class UserTeacherFactory(UserFactory):
    """User Teacher Factory
    """
    class Meta:
        model = 'accounts.User'

    status = 'TE'


class TeacherFactory(factory.django.DjangoModelFactory):
    """Teacher Factory
    """
    class Meta:
        model = 'accounts.Teacher'

    user = factory.SubFactory(UserTeacherFactory)


class UserSchoolAdminFactory(UserFactory):
    """User School Admin Factory
    """
    class Meta:
        model = 'accounts.User'

    status = 'SA'


class SchoolAdminFactory(factory.django.DjangoModelFactory):
    """School Admin Factory
    """
    class Meta:
        model = 'accounts.SchoolAdmin'

    user = factory.SubFactory(UserSchoolAdminFactory)


class TestSetUp(APITestCase):
    """ Test set up class
    test set up test data for school app
    """
    @classmethod
    def setUpTestData(cls):
        """School App Test data
        변수 이름 규칙
        학교 이름 : school + 숫자 형태
        이외의 학생, 교사, 수업 등은 학교 이름의 숫자에 따름

        수업
        학교1에 속하는 수업은 수업1_1, 수업1_2 형태
        학교2에 속하는 수업은 수업2_1, 수업2_1 형태
        """
        # basic data
        cls.test_password = 'test1234!'
        cls.jwt_url = reverse('JWT_login')
        cls.content_type = 'application/json'

        # objects
        cls.school1 = SchoolFactory()
        cls.school2 = SchoolFactory()
        cls.lecture1_1 = LectureFactory(school=cls.school1)
        cls.lecture1_2 = LectureFactory(school=cls.school1)
        cls.lecture2_1 = LectureFactory(school=cls.school2)
        cls.classroom1_1 = ClassroomFactory(school=cls.school1)
        cls.classroom1_2 = ClassroomFactory(school=cls.school1)
        cls.classroom2_1 = ClassroomFactory(school=cls.school2)

        cls.student1 = StudentFactory()
        cls.student1.school = cls.school1
        cls.student1.lecture_list.add(cls.lecture1_1)
        cls.student1.classroom = cls.classroom1_1
        cls.student1.save()

        cls.school_admin1 = SchoolAdminFactory()
        cls.school_admin1.school = cls.school1
        cls.school_admin1.save()
        
        cls.teacher1 = TeacherFactory()
        cls.teacher1.school = cls.school1
        cls.teacher1.lecture = cls.lecture1_1
        cls.teacher1.classroom = cls.classroom1_1
        cls.teacher1.save()
        
        cls.teacher1_2 = TeacherFactory()
        cls.teacher1_2.school = cls.school1
        cls.teacher1_2.lecture = cls.lecture1_2
        cls.teacher1_2.classroom = cls.classroom1_2
        cls.teacher1_2.save()
        
        cls.teacher2_1 = TeacherFactory()
        cls.teacher2_1.school = cls.school2
        cls.teacher2_1.lecture = cls.lecture2_1
        cls.teacher2_1.classroom = cls.classroom2_1
        cls.teacher2_1.save()
        
        cls.lecture1_1.teacher = cls.teacher1
        cls.lecture1_2.teacher = cls.teacher1_2
        cls.lecture2_1.teacher = cls.teacher2_1

        cls.lecture1_1.save()
        cls.lecture1_2.save()
        cls.lecture2_1.save()

        # JSON data for JWT
        cls.student1_info = {
            'username': cls.student1.user.username,
            'password': cls.test_password,
        }
        cls.student1_info_json = json.dumps(cls.student1_info)

        cls.school_admin1_info = {
            'username': cls.school_admin1.user.username,
            'password': cls.test_password,
        }
        cls.school_admin1_info_json = json.dumps(cls.school_admin1_info)

        cls.teacher1_info = {
            'username': cls.teacher1.user.username,
            'password': cls.test_password,
        }
        cls.teacher1_info_json = json.dumps(cls.teacher1_info)

        cls.lecture_data = {
            'name': 'test',#cls.lecture1_1.name,
            'time_list': {'test':'test'},#cls.lecture1_1.time_list,
            'teacher' : cls.teacher1.pk,
            'student_list': [cls.student1.pk],
        }
        cls.lecture_data_json = json.dumps(cls.lecture_data)