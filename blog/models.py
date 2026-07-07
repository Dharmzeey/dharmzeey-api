from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(help_text="Rich HTML — code snippets, images, video embeds.")
    excerpt = models.TextField(max_length=500, blank=True, help_text="Short summary for list pages and SEO.")
    featured_image = models.URLField(blank=True, help_text="Backblaze / S3 URL for the hero image.")
    featured_image_alt = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    published_date = models.DateTimeField(db_index=True)
    is_published = models.BooleanField(default=False, db_index=True)
    read_time_minutes = models.PositiveSmallIntegerField(default=0)
    meta_title = models.CharField(max_length=70, blank=True, help_text="SEO title (defaults to title).")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title[:70]
        super().save(*args, **kwargs)
