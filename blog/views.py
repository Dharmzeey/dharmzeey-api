from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import BlogPost, Tag
from .serializers import (
    BlogPostDetailSerializer,
    BlogPostListSerializer,
    BlogPostWriteSerializer,
    TagSerializer,
)


class BlogPostListView(generics.ListAPIView):
    serializer_class = BlogPostListSerializer

    def get_queryset(self):
        qs = BlogPost.objects.filter(is_published=True).prefetch_related("tags")
        tag_slug = self.request.query_params.get("tag")
        if tag_slug:
            qs = qs.filter(tags__slug=tag_slug)
        return qs


class BlogPostDetailView(generics.RetrieveAPIView):
    serializer_class = BlogPostDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).prefetch_related("tags")


class BlogPostCreateView(generics.CreateAPIView):
    serializer_class = BlogPostWriteSerializer
    permission_classes = [permissions.IsAdminUser]


class BlogPostUpdateView(generics.UpdateAPIView):
    serializer_class = BlogPostWriteSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "slug"
    queryset = BlogPost.objects.all()


class BlogPostDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "slug"
    queryset = BlogPost.objects.all()


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def recent_posts(request):
    """Return the 4 most recent published posts (for homepage Writing section)."""
    posts = BlogPost.objects.filter(is_published=True).prefetch_related("tags")[:4]
    serializer = BlogPostListSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def related_posts(request, slug):
    """Return 3 published posts excluding the current one."""
    posts = (
        BlogPost.objects.filter(is_published=True)
        .exclude(slug=slug)
        .prefetch_related("tags")[:3]
    )
    serializer = BlogPostListSerializer(posts, many=True)
    return Response(serializer.data)


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
