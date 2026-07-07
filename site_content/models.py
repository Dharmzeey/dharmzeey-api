from django.db import models


class SiteContent(models.Model):
    key = models.SlugField(max_length=100, unique=True, help_text="Identifier: 'hero', 'about', 'contact', etc.")
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True, help_text="Rich HTML content.")
    metadata = models.JSONField(default=dict, blank=True, help_text="Arbitrary key-value data, e.g. stats grid.")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "site content"

    def __str__(self):
        return self.key
