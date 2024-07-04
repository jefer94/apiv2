# Generated by Django 3.2.18 on 2023-04-29 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("marketing", "0067_course_status_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="formentry",
            name="ac_deal_course",
            field=models.CharField(
                blank=True,
                default=None,
                help_text="If != course it means it was updated later on CRM",
                max_length=100,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="formentry",
            name="ac_deal_location",
            field=models.CharField(
                blank=True,
                default=None,
                help_text="If != location it means it was updated later on CRM",
                max_length=50,
                null=True,
            ),
        ),
    ]
