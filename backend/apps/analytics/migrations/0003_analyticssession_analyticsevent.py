import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("analytics", "0002_dailysitevisit")]

    operations = [
        migrations.CreateModel(
            name="AnalyticsSession",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("visitor_id", models.UUIDField(db_index=True)),
                ("started_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("last_seen_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("landing_path", models.CharField(blank=True, max_length=512)),
                ("referrer", models.URLField(blank=True, max_length=1000)),
                ("source", models.CharField(db_index=True, default="Direct", max_length=80)),
                ("utm_source", models.CharField(blank=True, max_length=160)),
                ("utm_medium", models.CharField(blank=True, max_length=160)),
                ("utm_campaign", models.CharField(blank=True, max_length=160)),
                ("device_type", models.CharField(choices=[("desktop", "Desktop"), ("mobile", "Mobile"), ("tablet", "Tablet")], default="desktop", max_length=16)),
                ("browser", models.CharField(blank=True, max_length=80)),
                ("operating_system", models.CharField(blank=True, max_length=80)),
                ("language", models.CharField(blank=True, max_length=35)),
                ("country", models.CharField(blank=True, max_length=2)),
                ("is_returning", models.BooleanField(db_index=True, default=False)),
            ],
            options={
                "ordering": ["-started_at"],
                "indexes": [
                    models.Index(fields=["visitor_id", "started_at"], name="analytics_visitor_started"),
                    models.Index(fields=["source", "started_at"], name="analytics_source_started"),
                ],
            },
        ),
        migrations.CreateModel(
            name="AnalyticsEvent",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("event_type", models.CharField(choices=[("page_view", "Page view"), ("project_view", "Project view"), ("contact_click", "Contact click"), ("github_click", "GitHub click"), ("linkedin_click", "LinkedIn click"), ("cv_download", "CV download")], db_index=True, max_length=32)),
                ("path", models.CharField(blank=True, db_index=True, max_length=512)),
                ("target", models.CharField(blank=True, max_length=512)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("session", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="events", to="analytics.analyticssession")),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["event_type", "created_at"], name="analytics_event_created"),
                    models.Index(fields=["path", "created_at"], name="analytics_path_created"),
                ],
            },
        ),
    ]
