# Generated by Django 3.0.8 on 2020-07-17 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("freelance", "0002_auto_20200717_2003"),
    ]

    operations = [
        migrations.AlterField(
            model_name="issue",
            name="body",
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name="issue",
            name="title",
            field=models.CharField(max_length=255),
        ),
    ]
