# Generated by Django 5.0.2 on 2024-03-06 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0079_alter_coursetranslation_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='plan_slug',
            field=models.SlugField(blank=True, default=None, max_length=150, null=True),
        ),
    ]
