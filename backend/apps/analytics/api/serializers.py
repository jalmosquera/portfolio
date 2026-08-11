from rest_framework import serializers


class VisitPeriodSerializer(serializers.Serializer):
    label = serializers.CharField()
    visits = serializers.IntegerField(min_value=0)


class VisitSummarySerializer(serializers.Serializer):
    today = serializers.IntegerField(min_value=0)
    current_week = serializers.IntegerField(min_value=0)
    current_month = serializers.IntegerField(min_value=0)
    all_time = serializers.IntegerField(min_value=0)
    daily = VisitPeriodSerializer(many=True)
    weekly = VisitPeriodSerializer(many=True)
    monthly = VisitPeriodSerializer(many=True)
