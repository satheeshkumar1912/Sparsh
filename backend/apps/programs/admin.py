from django.contrib import admin
from .models import Program, FeaturePillar


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "age_group", "is_featured", "is_published", "order")
    list_filter = ("category", "is_featured", "is_published")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(FeaturePillar)
class FeaturePillarAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_published")
    prepopulated_fields = {"slug": ("title",)}
