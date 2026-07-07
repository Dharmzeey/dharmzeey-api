from rest_framework import serializers

from .models import BlogPost, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class BlogPostListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id", "title", "slug", "excerpt", "featured_image",
            "featured_image_alt", "tags", "published_date",
            "read_time_minutes", "meta_title", "meta_description",
        ]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            "id", "title", "slug", "content", "excerpt",
            "featured_image", "featured_image_alt", "tags",
            "published_date", "read_time_minutes",
            "meta_title", "meta_description",
            "created_at", "updated_at",
        ]


class BlogPostWriteSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Tag.objects.all(), required=False,
    )

    class Meta:
        model = BlogPost
        fields = [
            "title", "slug", "content", "excerpt",
            "featured_image", "featured_image_alt", "tags",
            "published_date", "is_published", "read_time_minutes",
            "meta_title", "meta_description",
        ]
