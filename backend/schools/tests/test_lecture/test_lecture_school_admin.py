from django.urls import reverse
from rest_framework.views import status

from ..test_setup import TestSetUp, LectureFactory


class TestLectureSchoolAdmin(TestSetUp):
    """Test lecture School Admin
    school_admin1 기준으로 테스트 진행
    """
    def setUp(self) -> None:
        res = self.client.post(
            self.jwt_url,
            self.school_admin1_info_json,
            content_type=self.content_type
        )
        self.school_admin1_token = res.data.get('access')
        return super().setUp()

    def test_lecture_list(self):
        """수업 목록 조회
        JWT에 따라서 테스트 진행
        JWT를 사용하지 않고 lecture list 조회 >> 401
        JWT를 사용하여 조회 >> 200
        """
        # 401
        url = reverse('lecture_list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # 200
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.school_admin1_token}'
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_lecture_create(self):
        """수업 생성
        JWT 인증 후 진행
        학교 관리자만 가능하므로 >> 200
        부적절한 데이터 >> 400
        """
        url = reverse('lecture_list')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.school_admin1_token}'
        )
        res = self.client.post(
            url,
            data=self.lecture_data_json,
            content_type=self.content_type
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lecture_detail(self):
        """수업 상세 조회
        JWT 인증 후 진행
        자신의 학교의 수업 >> 200
        다른 학교의 수업 >> 401
        """
        url = reverse('lecture_detail', kwargs={'lecture_pk': self.lecture1_1.pk})
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.school_admin1_token}'
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # 401
        url = reverse('lecture_detail', kwargs={'lecture_pk': self.lecture2_1.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lecture_update(self):
        """수업 수정
        JWT 인증 후 진행
        학교 관리자만 가능하므로 >> 200
        다른 학교의 수업 수정 시도 >> 401
        """
        # 200
        url = reverse('lecture_detail', kwargs={'lecture_pk': self.lecture1_1.pk})
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.school_admin1_token}'
        )
        res = self.client.put(
            url,
            data=self.lecture_data_json,
            content_type=self.content_type
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # 401
        url = reverse('lecture_detail', kwargs={'lecture_pk': self.lecture2_1.pk})
        res = self.client.put(
            url,
            data=self.lecture_data_json,
            content_type=self.content_type
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lecture_delete(self):
        """수업 삭제
        JWT 인증 후 진행
        학교 관리자만 가능하므로 >> 200
        다른 학교 수업 삭제 >> 401
        없는 수업 삭제 >> 404
        """
        # 200
        tmp_lecture = LectureFactory(school=self.school1)
        url = reverse('lecture_detail', kwargs={'lecture_pk': tmp_lecture.pk})
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.school_admin1_token}'
        )
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # 401
        url = reverse('lecture_detail', kwargs={'lecture_pk': self.lecture2_1.pk})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # 404
        url = reverse('lecture_detail', kwargs={'lecture_pk': 50000})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
