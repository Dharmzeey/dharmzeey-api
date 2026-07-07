from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id", "title", "slug", "category", "intro", "summary",
            "image", "url", "github", "github_api", "stack",
            "sort_order", "created_at", "updated_at",
        ]


class ProjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "title", "slug", "category", "intro", "summary",
            "image", "url", "github", "github_api", "stack",
            "is_published", "sort_order",
        ]
