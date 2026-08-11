from django.urls import path

from .views import AnalyticsEventView, AnalyticsSessionView, RecordVisitView, VisitSummaryView


urlpatterns = [
    path("visits/", RecordVisitView.as_view(), name="record-visit"),
    path("analytics/sessions/", AnalyticsSessionView.as_view(), name="analytics-session"),
    path("analytics/events/", AnalyticsEventView.as_view(), name="analytics-event"),
    path("analytics/summary/", VisitSummaryView.as_view(), name="visit-summary"),
]
