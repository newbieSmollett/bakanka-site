from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "company", "source", "is_processed", "created_at")
    list_filter = ("is_processed", "source", "created_at")
    search_fields = ("name", "phone", "company", "comment")
    ordering = ("-created_at",)