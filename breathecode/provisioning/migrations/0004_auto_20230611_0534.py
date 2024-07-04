# Generated by Django 3.2.19 on 2023-06-11 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("provisioning", "0003_auto_20230530_1832"),
    ]

    operations = [
        migrations.AddField(
            model_name="provisioningactivity",
            name="hash",
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="provisioningbill",
            name="status",
            field=models.CharField(
                choices=[
                    ("DUE", "Due"),
                    ("DISPUTED", "Disputed"),
                    ("IGNORED", "Ignored"),
                    ("PENDING", "Pending"),
                    ("PAID", "Paid"),
                    ("ERROR", "Error"),
                ],
                default="DUE",
                max_length=20,
            ),
        ),
    ]
