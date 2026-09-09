from django.contrib import admin
from .models import Testimonial, SiteStat, GalleryItem, FAQ, ContactMessage


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
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read",)
    readonly_fields = ("created_at",)
