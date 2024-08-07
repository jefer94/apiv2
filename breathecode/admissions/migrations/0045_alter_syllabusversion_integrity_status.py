# Generated by Django 3.2.15 on 2022-09-16 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admissions", "0044_auto_20220912_1928"),
    ]

    operations = [
        migrations.AlterField(
            model_name="syllabusversion",
            name="integrity_status",
            field=models.CharField(
                choices=[("ERROR", "Error"), ("PENDING", "Pending"), ("WARNING", "Warning"), ("OK", "Ok")],
                default="PENDING",
                max_length=15,
            ),
        ),
    ]
