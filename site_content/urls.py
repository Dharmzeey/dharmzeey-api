from django.urls import path

from . import views

app_name = "site_content"

urlpatterns = [
    path("", views.SiteContentListView.as_view(), name="list"),
    path("bundle/", views.site_bundle, name="bundle"),
    path("<slug:key>/", views.SiteContentDetailView.as_view(), name="detail"),
    path("<slug:key>/update/", views.SiteContentUpdateView.as_view(), name="update"),
]
