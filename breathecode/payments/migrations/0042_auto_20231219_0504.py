# Generated by Django 3.2.23 on 2023-12-19 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0041_auto_20231218_1945"),
    ]

    operations = [
        migrations.AlterField(
            model_name="financialreputation",
            name="in_4geeks",
            field=models.CharField(
                choices=[("GOOD", "Good"), ("BAD", "BAD"), ("FRAUD", "Fraud"), ("UNKNOWN", "Unknown")],
                default="GOOD",
                help_text="4Geeks reputation",
                max_length=17,
            ),
        ),
        migrations.AlterField(
            model_name="financialreputation",
            name="in_stripe",
            field=models.CharField(
                choices=[("GOOD", "Good"), ("BAD", "BAD"), ("FRAUD", "Fraud"), ("UNKNOWN", "Unknown")],
                default="GOOD",
                help_text="Stripe reputation",
                max_length=17,
            ),
        ),
    ]
