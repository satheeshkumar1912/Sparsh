import csv
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.utils import timezone
from .models import Testimonial, SiteStat, GalleryItem, FAQ, ContactMessage


def generate_contact_messages_csv(queryset):
    """Generates an HttpResponse containing CSV report for given ContactMessage queryset."""
    now_str = timezone.localtime(timezone.now()).strftime("%Y%m%d_%H%M%S")
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = (
        f'attachment; filename="sparsh_contact_messages_report_{now_str}.csv"'
    )

    # Write UTF-8 BOM for Microsoft Excel compatibility
    response.write("\ufeff")

    writer = csv.writer(response)
    writer.writerow([
        "Message ID",
        "Submitted At (IST)",
        "Sender Name",
        "Email Address",
        "Phone Number",
        "Subject",
        "Message",
        "Read Status",
    ])

    for item in queryset:
        created_at_str = (
            timezone.localtime(item.created_at).strftime("%Y-%m-%d %I:%M %p")
            if item.created_at
            else ""
        )
        writer.writerow([
            item.id,
            created_at_str,
            item.name,
            item.email,
            item.phone or "",
            item.subject,
            item.message,
            "Read" if item.is_read else "Unread",
        ])

    return response


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("parent_name", "program", "is_featured", "consent_given", "is_published")
    list_filter = ("is_featured", "consent_given", "is_published")


@admin.register(SiteStat)
class SiteStatAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteStat.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "caption", "order", "is_published")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "order", "is_published")
    list_filter = ("category",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    change_list_template = "admin/content/contactmessage/change_list.html"
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "phone", "subject", "message")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    actions = ["export_as_csv"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "download-csv/",
                self.admin_site.admin_view(self.download_csv_view),
                name="content_contactmessage_download_csv",
            ),
        ]
        return custom_urls + urls

    def download_csv_view(self, request):
        """Exports currently filtered or all contact messages to CSV."""
        cl = self.get_changelist_instance(request)
        queryset = cl.get_queryset(request)
        return generate_contact_messages_csv(queryset)

    @admin.action(description="Download selected messages as CSV report")
    def export_as_csv(self, request, queryset):
        return generate_contact_messages_csv(queryset)
