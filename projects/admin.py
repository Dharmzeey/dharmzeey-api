from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "sort_order")
    list_filter = ("is_published",)
    list_editable = ("sort_order", "is_published")
    search_fields = ("title", "category", "intro")
    prepopulated_fields = {"slug": ("title",)}
