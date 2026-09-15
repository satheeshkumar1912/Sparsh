import csv
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.utils import timezone
from .models import AdmissionEnquiry


def generate_enquiries_csv(queryset):
    """Generates an HttpResponse containing CSV report for given AdmissionEnquiry queryset."""
    now_str = timezone.localtime(timezone.now()).strftime("%Y%m%d_%H%M%S")
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = (
        f'attachment; filename="sparsh_admission_enquiries_report_{now_str}.csv"'
    )

    # Write UTF-8 BOM for Microsoft Excel compatibility
    response.write("\ufeff")

    writer = csv.writer(response)
    writer.writerow([
        "Enquiry ID",
        "Submitted At (IST)",
        "Child Name",
        "Age",
        "Learning Needs & Support",
        "Program of Interest",
        "Parent / Guardian Name",
        "Parent Email",
        "Parent Phone",
        "Preferred Contact Mode",
        "Additional Message",
        "Status",
        "Privacy Consent",
        "Staff Notes",
        "IP Address",
    ])

    for item in queryset:
        created_at_str = (
            timezone.localtime(item.created_at).strftime("%Y-%m-%d %I:%M %p")
            if item.created_at
            else ""
        )
        contact_display = (
            item.get_preferred_contact_display()
            if hasattr(item, "get_preferred_contact_display")
            else item.preferred_contact
        )
        status_display = (
            item.get_status_display()
            if hasattr(item, "get_status_display")
            else item.status
        )
        writer.writerow([
            item.id,
            created_at_str,
            item.child_name,
            item.age,
            item.needs,
            item.program_of_interest,
            item.parent_name,
            item.parent_email,
            item.parent_phone,
            contact_display,
            item.message,
            status_display,
            "Yes" if item.consent_privacy else "No",
            item.notes,
            item.ip_address or "",
        ])

    return response


@admin.register(AdmissionEnquiry)
class AdmissionEnquiryAdmin(admin.ModelAdmin):
    change_list_template = "admin/admissions/admissionenquiry/change_list.html"
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
    actions = ["export_as_csv"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "download-csv/",
                self.admin_site.admin_view(self.download_csv_view),
                name="admissions_admissionenquiry_download_csv",
            ),
        ]
        return custom_urls + urls

    def download_csv_view(self, request):
        """Exports currently filtered or all enquiries to CSV."""
        cl = self.get_changelist_instance(request)
        queryset = cl.get_queryset(request)
        return generate_enquiries_csv(queryset)

    @admin.action(description="Download selected enquiries as CSV report")
    def export_as_csv(self, request, queryset):
        return generate_enquiries_csv(queryset)
