from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("adedamola/", admin.site.urls),
    path("api/blog/", include("blog.urls")),
    path("api/projects/", include("projects.urls")),
    path("api/skills/", include("skills.urls")),
    path("api/content/", include("site_content.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
