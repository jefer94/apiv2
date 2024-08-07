# Generated by Django 3.2.16 on 2023-01-09 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admissions", "0049_auto_20221229_1616"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cohort",
            name="is_hidden_on_prework",
            field=models.BooleanField(
                blank=True,
                default=True,
                help_text="Determines if the cohort will be shown in the dashboard if it's status is 'PREWORK'",
                null=True,
            ),
        ),
    ]
