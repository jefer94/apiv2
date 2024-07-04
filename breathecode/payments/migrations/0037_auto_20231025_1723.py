# Generated by Django 3.2.22 on 2023-10-25 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0036_merge_20230926_0017"),
    ]

    operations = [
        migrations.AddField(
            model_name="consumable",
            name="sort_priority",
            field=models.IntegerField(
                default=1, help_text="(e.g. 1, 2, 3, ...) It is going to be used to sort the items on the frontend"
            ),
        ),
        migrations.AddField(
            model_name="serviceitem",
            name="sort_priority",
            field=models.IntegerField(
                default=1, help_text="(e.g. 1, 2, 3, ...) It is going to be used to sort the items on the frontend"
            ),
        ),
    ]
