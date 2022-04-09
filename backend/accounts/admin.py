from django.contrib import admin
from django.contrib.admin import ModelAdmin 
from django.contrib.auth.admin import UserAdmin
from django.db.models.functions import Lower
from .models import User, Student, Teacher, SchoolAdmin, FriendRequest

# Register your models here.
class StudentInline(admin.TabularInline):
    model = Student


class TeacherInline(admin.TabularInline):
    model = Teacher


class SchoolAdminInline(admin.TabularInline):
    model = SchoolAdmin


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'username', 'first_name', 'school_name', 'status')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom fields', {'fields': ('status', 'friend_list', 'profile_image',)}),
    )
    list_display_links = ('username',)
    list_filter = ('status',)
    ordering = ('-id',)
    inlines = [
        StudentInline, TeacherInline, SchoolAdminInline,
    ]

    def school_name(self, user):
        if user.status == 'ST':
            return user.student.school
        elif user.status == 'TE':
            return user.teacher.school
        elif user.status == 'SA':
            return user.school_admin.school
        return None


@admin.register(FriendRequest)
class FriendRequestAdmin(ModelAdmin):
    list_display = ('id', 'request_status', 'from_user_detail', 'to_user_detail')
    list_display_links = ('request_status',)
    list_filter = ('request_status',)
    fields = (('from_user', 'to_user'), 'request_status',)
    
    def from_user_detail(self, request):
        return f'id: {request.from_user.pk} / username: {request.from_user}'
    
    def to_user_detail(self, request):
        return f'id: {request.to_user.pk} / username: {request.to_user}'


admin.site.register(User, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)


@admin.register(SchoolAdmin)
class SchoolAdminAdmin(ModelAdmin):
    list_display = ('user', 'school', 'account_type',)
    list_filter = ('account_type',)
