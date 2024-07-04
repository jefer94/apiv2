# Generated by Django 3.2.16 on 2022-11-29 23:54

import breathecode.utils.validators.language
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authenticate", "0028_auto_20220704_0322"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserSetting",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "lang",
                    models.CharField(
                        default="en",
                        max_length=5,
                        validators=[breathecode.utils.validators.language.validate_language_code],
                    ),
                ),
            ],
        ),
    ]
