from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "company", "status", "source", "created_at")
    list_filter = ("status", "source", "created_at")
    search_fields = ("name", "phone", "company", "comment", "ip_address", "user_agent")
    ordering = ("-created_at",)