from django.db.models import F
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.i18n import request_language

from ..models import Resume
from ..pdf import build_resume_pdf
from .serializers import ResumeDownloadQuerySerializer, ResumeSerializer


class ResumeDetailView(APIView):
    serializer_class = ResumeSerializer

    def get(self, request):
        resume = Resume.objects.filter(is_active=True).first()
        if not resume:
            return Response({"detail": "CV not available."}, status=status.HTTP_404_NOT_FOUND)
        return Response(ResumeSerializer(resume).data)


class ResumeDownloadView(APIView):
    serializer_class = ResumeDownloadQuerySerializer

    def get(self, request):
        query = ResumeDownloadQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        resume = Resume.objects.filter(is_active=True).first()
        if not resume:
            return Response({"detail": "CV not available."}, status=status.HTTP_404_NOT_FOUND)

        language = request_language(request)
        variant = query.validated_data["variant"]
        pdf = build_resume_pdf(resume, variant=variant, language=language)
        Resume.objects.filter(pk=resume.pk).update(download_count=F("download_count") + 1)
        stem = resume.public_filename.removesuffix(".pdf")
        return FileResponse(
            pdf,
            as_attachment=True,
            filename=f"{stem}_{variant}.pdf",
            content_type="application/pdf",
        )
