from django.urls import path

from .views import ResumeDetailView, ResumeDownloadView


urlpatterns = [
    path("cv/", ResumeDetailView.as_view(), name="resume-detail"),
    path("cv/download/", ResumeDownloadView.as_view(), name="resume-download"),
]
