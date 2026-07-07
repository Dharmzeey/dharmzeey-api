from django.contrib import admin

from .models import BlogPost, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_date", "read_time_minutes")
    list_filter = ("is_published", "tags")
    search_fields = ("title", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_date"
    filter_horizontal = ("tags",)
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "content", "excerpt", "tags"),
        }),
        ("Media", {
            "fields": ("featured_image", "featured_image_alt"),
        }),
        ("Publishing", {
            "fields": ("is_published", "published_date", "read_time_minutes"),
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description"),
            "classes": ("collapse",),
        }),
    )
