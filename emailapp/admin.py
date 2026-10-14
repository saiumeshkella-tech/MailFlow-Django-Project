from django.contrib import admin
from .models import UserProfile, EmailRecord

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")

@admin.register(EmailRecord)
class EmailRecordAdmin(admin.ModelAdmin):
    list_display = ("recipient_name", "recipient_email", "subject", "status", "created_at")
    list_filter = ("status", "tone", "created_at")
    search_fields = ("recipient_name", "recipient_email", "subject")
