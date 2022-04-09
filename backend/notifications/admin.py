from django.contrib import admin
from .models import Notification

# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Notification Admin
    """
    list_display = ('id', 'user', 'notification_type', 'read',)
    list_display_links = ('user',)
    list_filter = ('user',)
    search_fields = ('user',)
