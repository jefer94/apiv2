# Generated by Django 3.2.19 on 2023-07-18 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("provisioning", "0009_provisioninguserconsumption_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="provisioninguserconsumption",
            name="quantity",
            field=models.FloatField(default=0),
        ),
    ]
