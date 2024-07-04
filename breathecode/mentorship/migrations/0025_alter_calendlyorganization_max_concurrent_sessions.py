# Generated by Django 3.2.18 on 2023-08-21 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mentorship", "0024_auto_20230821_1922"),
    ]

    operations = [
        migrations.AlterField(
            model_name="calendlyorganization",
            name="max_concurrent_sessions",
            field=models.IntegerField(
                blank=True,
                default=None,
                help_text="For example: Users will only be allowed to book 2 sessions per service at a time, they will have to wait for sessions to complete (or cancel) before booking again",
                null=True,
            ),
        ),
    ]
