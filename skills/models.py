from django.db import models


class SkillCategory(models.Model):
    label = models.CharField(max_length=100, help_text="e.g. '// frontend'")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name_plural = "skill categories"

    def __str__(self):
        return self.label


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=120, help_text="e.g. 'Next.js / App Router'")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.name
