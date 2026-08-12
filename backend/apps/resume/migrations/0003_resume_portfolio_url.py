from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resume", "0002_alter_resume_options_remove_resume_file_resume_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="resume",
            name="portfolio_url",
            field=models.URLField(
                blank=True,
                default="https://portfolio.mosquerasoft.com/",
                max_length=300,
            ),
        ),
    ]
