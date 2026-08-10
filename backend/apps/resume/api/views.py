from django.db.models import F
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Resume
from .serializers import ResumeSerializer


class ResumeDetailView(APIView):
    def get(self, request):
        resume = Resume.objects.first()
        if not resume or not resume.file:
            return Response({"detail": "CV not available."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ResumeSerializer(resume).data)


class ResumeDownloadView(APIView):
    def get(self, request):
        resume = Resume.objects.first()
        if not resume or not resume.file:
            return Response({"detail": "CV not available."}, status=status.HTTP_404_NOT_FOUND)

        Resume.objects.filter(pk=resume.pk).update(download_count=F("download_count") + 1)
        return FileResponse(
            resume.file.open("rb"),
            as_attachment=True,
            filename=resume.public_filename,
            content_type="application/pdf",
        )
