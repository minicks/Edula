import json

from django.urls import reverse

from rest_framework.views import status

from .test_setups import TestSetUp


class TestStudent(TestSetUp):
    """
    Test Student
    """
    def setUp(self) -> None:
        res = self.client.post(
            self.jwt_url,
            self.student_info_json,
            content_type=self.content_type,
        )
        self.student_token = res.data.get('access')
        self.student_refresh_token = res.data.get('refresh')
        return super().setUp()

    def test_token_without_data(self):
        """
        JWT 발급 검사
        """
        url = reverse('JWT_login')
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_toekn_with_data(self):
        """
        JWT 발급 검사
        """
        url = reverse('JWT_login')
        res = self.client.post(
            url,
            self.student_info_json,
            content_type=self.content_type,
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        """
        JWT 재발급
        """
        url = reverse('JWT_refresch')
        res = self.client.post(
            url,
            json.dumps({'refresh': self.student_refresh_token}),
            content_type=self.content_type,
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_information(self):
        """
        유저 정보 조회
        """
        # student
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.student_token}'
        )
        url = reverse('user_self_information')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


# class TestTeacher(TestSetUp):
#     """
#     Test Teacher
#     """
#     def setUp(self) -> None:
#         res = self.client.post(
#             self.jwt_url,
#             self.teacher_info_json,
#             content_type=self.content_type,
#         )
#         self.teacher_token = res.data.get('access')
#         self.teacher_refresh_token = res.data.get('refresh')
#         return super().setUp()

#     def test_token_without_data(self):
#         """
#         JWT 발급 검사
#         """
#         url = reverse('JWT_login')
#         res = self.client.post(url)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_toekn_with_data(self):
#         """
#         JWT 발급 검사
#         """
#         url = reverse('JWT_login')
#         res = self.client.post(
#             url,
#             self.teacher_info_json,
#             content_type=self.content_type,
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

#     def test_refresh_token(self):
#         """
#         JWT 재발급
#         """
#         url = reverse('JWT_refresch')
#         res = self.client.post(
#             url,
#             json.dumps({'refresh': self.teacher_refresh_token}),
#             content_type=self.content_type,
#         )
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

#     def test_user_information(self):
#         """
#         유저 정보 조회
#         """
#         # teacher
#         self.client.credentials(
#             HTTP_AUTHORIZATION=f'JWT {self.teacher_token}'
#         )
#         url = reverse('user_self_information')
#         res = self.client.get(url)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
'''
        # teacher
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.teacher_token}'
        )
        url = reverse('user_self_information')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # school admin
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.school_admin_token}'
        )
        url = reverse('user_self_information')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
'''    
