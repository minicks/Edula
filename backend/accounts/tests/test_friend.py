import json

from django.urls import reverse
from rest_framework.views import status

from .test_setups import TestSetUp


class TestFriend(TestSetUp):
    """
    Test friend
    """
    def setUp(self) -> None:
        res = self.client.post(
            self.jwt_url,
            self.student_info_json,
            content_type=self.content_type,
        )
        self.student_token = res.data.get('access')
        return super().setUp()

    def test_find_friend(self):
        """
        친구 찾기
        """
        url = reverse('friend_search', kwargs={'search': '싸피'})
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.student_token}'
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['student_count'], 0)
