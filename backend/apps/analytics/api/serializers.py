from rest_framework import serializers

from ..models import AnalyticsEvent, AnalyticsSession


class AnalyticsSessionSerializer(serializers.Serializer):
    visitor_id = serializers.UUIDField()
    session_id = serializers.UUIDField(required=False, allow_null=True)
    landing_path = serializers.CharField(max_length=512, required=False, allow_blank=True, default="")
    referrer = serializers.URLField(max_length=1000, required=False, allow_blank=True, default="")
    utm_source = serializers.CharField(max_length=160, required=False, allow_blank=True, default="")
    utm_medium = serializers.CharField(max_length=160, required=False, allow_blank=True, default="")
    utm_campaign = serializers.CharField(max_length=160, required=False, allow_blank=True, default="")
    device_type = serializers.ChoiceField(choices=AnalyticsSession.DeviceType.choices, default=AnalyticsSession.DeviceType.DESKTOP)
    browser = serializers.CharField(max_length=80, required=False, allow_blank=True, default="")
    operating_system = serializers.CharField(max_length=80, required=False, allow_blank=True, default="")
    language = serializers.CharField(max_length=35, required=False, allow_blank=True, default="")


class AnalyticsEventSerializer(serializers.Serializer):
    session_id = serializers.PrimaryKeyRelatedField(source="session", queryset=AnalyticsSession.objects.all())
    event_type = serializers.ChoiceField(choices=AnalyticsEvent.EventType.choices)
    path = serializers.CharField(max_length=512, required=False, allow_blank=True, default="")
    target = serializers.CharField(max_length=512, required=False, allow_blank=True, default="")


class VisitPeriodSerializer(serializers.Serializer):
    label = serializers.CharField()
    visits = serializers.IntegerField(min_value=0)
    unique_visitors = serializers.IntegerField(min_value=0, required=False, default=0)


class VisitSummarySerializer(serializers.Serializer):
    today = serializers.IntegerField(min_value=0)
    current_week = serializers.IntegerField(min_value=0)
    current_month = serializers.IntegerField(min_value=0)
    all_time = serializers.IntegerField(min_value=0)
    daily = VisitPeriodSerializer(many=True)
    weekly = VisitPeriodSerializer(many=True)
    monthly = VisitPeriodSerializer(many=True)
    unique_visitors = serializers.IntegerField(min_value=0, required=False, default=0)
    sessions = serializers.IntegerField(min_value=0, required=False, default=0)
    pageviews = serializers.IntegerField(min_value=0, required=False, default=0)
    pages_per_session = serializers.FloatField(min_value=0, required=False, default=0)
    average_session_seconds = serializers.IntegerField(min_value=0, required=False, default=0)
    bounce_rate = serializers.FloatField(min_value=0, max_value=100, required=False, default=0)
    new_visitors = serializers.IntegerField(min_value=0, required=False, default=0)
    returning_visitors = serializers.IntegerField(min_value=0, required=False, default=0)
    sources = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    devices = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    browsers = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    operating_systems = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    countries = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    top_pages = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    top_projects = serializers.ListField(child=serializers.DictField(), required=False, default=list)
    conversions = serializers.DictField(child=serializers.IntegerField(min_value=0), required=False, default=dict)
