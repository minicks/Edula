from django.urls import reverse
from rest_framework.views import status

from ..test_setup import TestSetUp


class TestClassroomStudent(TestSetUp):
    """Test Classroom Student
    student1 기준으로 테스트 진행
    """
    def setUp(self) -> None:
        res = self.client.post(
            self.jwt_url,
            self.student1_info_json,
            content_type=self.content_type
        )
        self.student1_token = res.data.get('access')
        return super().setUp()

    def test_classroom_list(self):
        """교실 전체 목록 조회
        JWT에 따라서 테스트 진행
        JWT를 사용하지 않고 lecture list 조회 >> 401
        JWT를 사용하고 조회 >> 200
        """
        # 401
        url = reverse('classroom_list', kwargs={'school_pk': self.school1.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # 200
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.student1_token}'
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_classroom_create(self):
        """교실 생성
        JWT 인증 후 진행
        학교 관리자만 가능하므로 >> 401
        """
        url = reverse('classroom_list', kwargs={'school_pk': self.school1.pk})
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_classroom_detail(self):
        """교실 상세 조회
        JWT 인증 후 진행
        자신이 속한 교실 + 속한 학교의 교실 >> 200
        자신이 속하지 않은 교실(같은 학교, 다른학교) >> 401
        """
        # 200
        url = reverse('classroom_detail',
            kwargs={
                'school_pk': self.school1.pk,
                'classroom_pk': self.classroom1_1.pk,
            }
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.student1_token}'
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        url = reverse('classroom_detail',
            kwargs={
                'school_pk': self.school1.pk,
                'classroom_pk': self.classroom1_2.pk,
            }
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # 401
        url = reverse('classroom_detail',
            kwargs={
                'school_pk': self.school2.pk,
                'classroom_pk': self.classroom2_1.pk,
            }
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_classroom_update(self):
        """교실 수정
        JWT 인증 후 진행
        학교 관리자만 가능하므로 >> 401
        """
        url = reverse('classroom_detail',
            kwargs={
                'school_pk': self.school1.pk,
                'classroom_pk': self.classroom1_1.pk,
            }
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.student1_token}'
        )
        res = self.client.put(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_classroom_delete(self):
        """교실 삭제
        JWT 인증 후 진행
        학교 관리자만 가능하므로 >> 401
        """
        url = reverse('classroom_detail',
            kwargs={
                'school_pk': self.school1.pk,
                'classroom_pk': self.classroom1_1.pk,
            }
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.student1_token}'
        )
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
