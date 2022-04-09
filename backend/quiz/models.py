from operator import mod
from django.db import models

class Quiz(models.Model):
    writer = models.ForeignKey(
        'accounts.User',
        related_name='quiz_list',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    body = models.JSONField()
    answer = models.JSONField()
    
    def __str__(self):
        return self.title



class QuizSubmission(models.Model):
    submitter = models.ForeignKey(
        'accounts.User',
        related_name='quizsub_list',
        on_delete=models.CASCADE,
    )
    quiz = models.ForeignKey(
        Quiz,
        related_name='quizsub_list',
        on_delete=models.CASCADE,
    )
    answer = models.JSONField()
    # score = models.IntegerField()