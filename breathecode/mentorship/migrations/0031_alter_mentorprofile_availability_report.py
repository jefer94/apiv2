# Generated by Django 5.0.7 on 2024-08-09 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mentorship", "0030_alter_mentorshipservice_video_provider"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mentorprofile",
            name="availability_report",
            field=models.JSONField(blank=True, default=list, help_text="Mentor availability report"),
        ),
    ]
