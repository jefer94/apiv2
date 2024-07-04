# Generated by Django 3.2.16 on 2023-03-28 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("provisioning", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="provisioningvendor",
            name="invite_url",
            field=models.URLField(
                blank=True,
                default=None,
                help_text="Some vendors (like Gitpod) allow to share invite link to automatically join",
                null=True,
            ),
        ),
    ]
