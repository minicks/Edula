from django.db import models
from accounts.models import User

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(
        User,
        related_name='message_receive',
        on_delete=models.CASCADE,
    )
    from_user = models.ForeignKey(
        User,
        related_name='message_send',
        on_delete=models.CASCADE,
    )
    content = models.CharField(
        max_length=100,
    )
    time = models.DateTimeField(
        auto_now_add=True,
    )
    send = models.BooleanField()
    read = models.BooleanField(
        default=False
    )
