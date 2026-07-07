from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="list"),
    path("create/", views.ProjectCreateView.as_view(), name="create"),
    path("<slug:slug>/", views.ProjectDetailView.as_view(), name="detail"),
    path("<slug:slug>/update/", views.ProjectUpdateView.as_view(), name="update"),
    path("<slug:slug>/delete/", views.ProjectDeleteView.as_view(), name="delete"),
]
