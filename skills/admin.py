from django.contrib import admin

from .models import Skill, SkillCategory


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("label", "sort_order")
    list_editable = ("sort_order",)
    inlines = [SkillInline]
