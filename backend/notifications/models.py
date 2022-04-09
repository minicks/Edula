from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from schools.models import Lecture

# Create your models here.
class Notification(models.Model):
    """Notification Model
    """

    class NotificationType(models.TextChoices):
        """Notification Type Choices
        지금은 친구 추가 요청, 숙제 생성 및 수정, 숙제 제출만 사용
        추가적으로 친구, 게시글 등 활용할 수 있음
        """
        FRIEND = 'FR', _('Friend')
        FRIEND_REQUEST = 'FQ', _('Friend Request')
        LECTURE = 'LE', _('Lecture')
        HOMEWORK_CREATE = 'HC', _('Homework Create')
        HOMEWORK_UPDATE = 'HU', _('Homework Update')
        HOMEWORK_SUMBISSION = 'HS', _('Homework Submission')
        ARTICLE = 'AR', _('Article')

    user = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE,
    )
    notification_type = models.CharField(
        max_length=2,
        choices=NotificationType.choices,
    )
    content = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    from_user = models.ForeignKey(
        User,
        related_name='notifications_send',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    lecture = models.ForeignKey(
        Lecture,
        related_name='notifications',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    read = models.BooleanField(
        default=False
    )
