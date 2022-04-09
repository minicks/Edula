"""Model for schools app
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class School(models.Model):
    """
    School model
    """
    name = models.CharField(max_length=40)
    abbreviation = models.CharField(
        max_length=10,
        unique=True,
    )

    def __str__(self):
        return f'{self.name}'


class Classroom(models.Model):
    """
    Classroom model
    """
    class_grade = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(6),
        ]
    )
    class_num = models.IntegerField()
    school = models.ForeignKey(
        School,
        related_name="class_list",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.school} {self.class_grade}학년 {self.class_num}반'

    def get_teacher(self):
        try:
            return self.teacher
        except:
            return None


class Lecture(models.Model):
    """
    Lecture model
    """
    name = models.CharField(max_length=10)
    time_list = models.JSONField(
        null=True,
        blank=True,
    )
    school = models.ForeignKey(
        School,
        related_name="lecture_list",
        on_delete=models.CASCADE,
    )
    teacher = models.ForeignKey(
        'accounts.Teacher',
        related_name="lecture_list",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    student_list = models.ManyToManyField(
        'accounts.Student',
        related_name="lecture_list",
    )

    def __str__(self):
        return f'{self.school} {self.name}'


class Homework(models.Model):
    """
    Homework model
    """
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    writer = models.ForeignKey(
        'accounts.User',
        related_name='homework_list',
        on_delete=models.CASCADE,
    )
    lecture = models.ForeignKey(
        Lecture,
        related_name="homework_list",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title


class HomeworkSubmission(models.Model):
    """Homework submission model
    """

    homework = models.ForeignKey(
        Homework,
        related_name='submission',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=20)
    content = models.TextField()
    creted_at = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(
        'accounts.User',
        related_name='homework_submission_list',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.homework} : {self.title}'


class HomeworkSubmissionFiles(models.Model):
    """Homework Submission Files Model
    """

    def homework_submission_path(instance, filename):
        """Make homework submission media file path
        """
        return f'submission/{instance.homework_submission.pk}/{filename}'

    homework_submission = models.ForeignKey(
        HomeworkSubmission,
        related_name='homework_submission_files',
        on_delete=models.CASCADE
    )
    files = models.FileField(
        upload_to=homework_submission_path,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.files}'


class Article(models.Model):
    """
    Atricle model
    """
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notice = models.BooleanField(
        default=False,
    )
    writer = models.ForeignKey(
        'accounts.User',
        related_name='article_list',
        on_delete=models.CASCADE,
    )
    lecture = models.ForeignKey(
        Lecture,
        related_name="article_list",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title
