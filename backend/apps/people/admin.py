from django.contrib import admin
from .models import TeamMember, Advisor


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", "is_published")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "role")


@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialty", "affiliation", "order", "is_published")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "specialty")
