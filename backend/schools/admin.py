"""admin for schools app
"""
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from accounts.models import SchoolAdmin, Teacher, Student
from .models import (
    School, Classroom, Lecture,
    Homework, HomeworkSubmission, HomeworkSubmissionFiles,
    Article
)

# Register your models here.
class StudentInline(admin.TabularInline):
    """Student Inline
    """
    model = Student
    extra = 1


class SchoolAdminInline(admin.TabularInline):
    """School Admin Inline
    """
    model = SchoolAdmin


class TeacherInline(admin.TabularInline):
    """Teacher Inline
    """
    model = Teacher
    extra = 1


class HomeWorkSubmissionFilesInline(admin.TabularInline):
    """Homework Submission Files Inline
    """
    model = HomeworkSubmissionFiles
    extra = 1


@admin.register(School)
class CustomSchoolAdmin(ModelAdmin):
    """Custom School Admin
    """
    list_display = ('id', 'name', 'abbreviation', 'school_admin', 'teacher', 'student')
    list_display_links = ('name',)
    inlines = [
        SchoolAdminInline, TeacherInline, StudentInline
    ]

    def student(self, school):
        return f'{school.student_list.count()}명'

    def school_admin(self, school):
        return school.school_admin

    def teacher(self, school):
        return f'{school.teacher_list.count()}명'


@admin.register(Classroom)
class ClassroomAdmin(ModelAdmin):
    """Classroom Admin
    """
    list_display = ('id', 'classroom_name', 'school_detail',)
    list_display_links = ('classroom_name',)
    list_filter = ('school',)
    inlines = [
        TeacherInline, StudentInline
    ]

    def classroom_name(self, classroom):
        return f'{classroom.class_grade}학년 {classroom.class_num}반'

    def school_detail(self, classroom):
        return f'id : {classroom.school.pk} / name: {classroom.school}'


@admin.register(Lecture)
class LectureAdmin(ModelAdmin):
    """Lecture Admin
    """
    list_display = ('id', 'name', 'school_detail', 'teacher', 'student')
    list_display_links = ('name',)

    def student(self, lecture):
        return f'{lecture.student_list.count()}명'

    def school_detail(self, classroom):
        return f'id : {classroom.school.pk} / name: {classroom.school}'

@admin.register(Homework)
class HomeworkAdmin(ModelAdmin):
    """Homework Admin
    """
    list_display = ('id', 'title', 'created_at', 'deadline',)
    list_display_links = ('title',)


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(ModelAdmin):
    """Homework Sbumission Admin
    """
    list_display = ('id', 'title', 'homework', 'writer', 'file_exist',)
    list_display_links = ('title',)
    inlines = [
        HomeWorkSubmissionFilesInline
    ]

    @admin.display(
        boolean=True,
    )
    def file_exist(self, homework_submission):
        return True if homework_submission.homework_submission_files.all() else False


@admin.register(HomeworkSubmissionFiles)
class HomeworkSubmissionFilesAdmin(ModelAdmin):
    """Homework Submission Filew Admin
    """
    list_display = ('id', 'homework_submission', 'files',)
    list_display_link = ('homwork_submission',)


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    """Article Admin
    """
    list_display = ('id', 'title', 'lecture', 'writer', 'notice',)
    list_display_links = ('title',)

    @admin.display(
        boolean=True
    )
    def notice(self, article):
        return article.notice
