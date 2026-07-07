from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    category = models.CharField(max_length=255, help_text="e.g. 'E-commerce · Gadget Store'")
    intro = models.TextField(help_text="Short tagline / description.")
    summary = models.TextField(blank=True, help_text="Longer description for SEO meta.")
    image = models.CharField(max_length=500, blank=True, help_text="Backblaze / S3 URL or relative path (/images/...) for project screenshot.")
    url = models.URLField(blank=True, help_text="Live project URL.")
    github = models.URLField(blank=True, help_text="GitHub repo URL.")
    github_api = models.URLField(blank=True, help_text="API repo URL (optional).")
    stack = models.JSONField(default=list, help_text='Tech tags, e.g. ["Next.js","Django REST"]')
    is_published = models.BooleanField(default=True, db_index=True)
    sort_order = models.PositiveIntegerField(default=0, help_text="Lower = appears first.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
