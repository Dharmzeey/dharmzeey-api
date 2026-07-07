from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.BlogPostListView.as_view(), name="list"),
    path("recent/", views.recent_posts, name="recent"),
    path("tags/", views.TagListView.as_view(), name="tags"),
    path("create/", views.BlogPostCreateView.as_view(), name="create"),
    path("<slug:slug>/", views.BlogPostDetailView.as_view(), name="detail"),
    path("<slug:slug>/related/", views.related_posts, name="related"),
    path("<slug:slug>/update/", views.BlogPostUpdateView.as_view(), name="update"),
    path("<slug:slug>/delete/", views.BlogPostDeleteView.as_view(), name="delete"),
]
