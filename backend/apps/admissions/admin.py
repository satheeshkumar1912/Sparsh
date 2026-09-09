from django.contrib import admin
from .models import AdmissionEnquiry


@admin.register(AdmissionEnquiry)
class AdmissionEnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "child_name",
        "age",
        "parent_name",
        "parent_email",
        "program_of_interest",
        "status",
        "created_at",
    )
    list_filter = ("status", "preferred_contact", "created_at")
    search_fields = ("child_name", "parent_name", "parent_email", "parent_phone", "needs")
    readonly_fields = ("created_at", "updated_at", "ip_address", "user_agent")
    date_hierarchy = "created_at"
