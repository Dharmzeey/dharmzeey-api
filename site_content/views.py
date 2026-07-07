from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import SiteContent
from .serializers import SiteContentSerializer


class SiteContentListView(generics.ListAPIView):
    queryset = SiteContent.objects.all()
    serializer_class = SiteContentSerializer
    pagination_class = None


class SiteContentDetailView(generics.RetrieveAPIView):
    queryset = SiteContent.objects.all()
    serializer_class = SiteContentSerializer
    lookup_field = "key"


class SiteContentUpdateView(generics.UpdateAPIView):
    queryset = SiteContent.objects.all()
    serializer_class = SiteContentSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "key"


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def site_bundle(request):
    """Return all site content in one request (hero, about, contact, etc.)."""
    items = SiteContent.objects.all()
    data = {item.key: SiteContentSerializer(item).data for item in items}
    return Response(data)
