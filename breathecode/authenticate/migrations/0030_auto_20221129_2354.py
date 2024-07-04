# Generated by Django 3.2.16 on 2022-11-29 23:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("authenticate", "0029_usersetting"),
    ]

    operations = [
        migrations.AddField(
            model_name="usersetting",
            name="main_currency",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="payments.currency"
            ),
        ),
        migrations.AddField(
            model_name="usersetting",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, related_name="settings", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
