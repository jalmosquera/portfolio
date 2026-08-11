from django.urls import path

from .views import RecordVisitView, VisitSummaryView


urlpatterns = [
    path("visits/", RecordVisitView.as_view(), name="record-visit"),
    path("analytics/summary/", VisitSummaryView.as_view(), name="visit-summary"),
]
