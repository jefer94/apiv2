# Generated by Django 5.1.6 on 2025-03-18 18:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authenticate", "0068_alter_notfoundanongoogleuser_id_token"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="academyauthsettings",
            name="github_whitelist_exemption_users",
            field=models.ManyToManyField(
                blank=True,
                help_text="Users that will never be removed from GitHub organization regardless of their cohort status",
                related_name="github_whitelist_exemptions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
