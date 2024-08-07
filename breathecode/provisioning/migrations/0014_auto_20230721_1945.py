# Generated by Django 3.2.19 on 2023-07-21 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("provisioning", "0013_alter_provisioningbill_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="provisioningbill",
            name="ended_at",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="provisioningbill",
            name="started_at",
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
