# Generated by Django 3.2.15 on 2022-09-19 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("admissions", "0045_alter_syllabusversion_integrity_status"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("freelance", "0015_auto_20220608_0129"),
    ]

    operations = [
        migrations.CreateModel(
            name="AcademyFreelanceProject",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("repository", models.URLField(help_text="Github repo where the event occured", max_length=255)),
                (
                    "total_client_price",
                    models.FloatField(help_text="How much will the client be billed for each our on this project"),
                ),
                ("academy", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="admissions.academy")),
            ],
        ),
        migrations.CreateModel(
            name="FreelanceProjectMember",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("repository", models.URLField(help_text="Github repo url", max_length=255)),
                (
                    "total_cost_price",
                    models.FloatField(
                        blank=True,
                        default=None,
                        help_text="Paid to the freelancer, leave blank to use the default freelancer price",
                        null=True,
                    ),
                ),
                (
                    "total_client_price",
                    models.FloatField(
                        blank=True,
                        default=None,
                        help_text="Billed to the client on this project/freelancer, leave blank to use default from the project",
                        null=True,
                    ),
                ),
                (
                    "freelancer",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="freelance.freelancer"),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="freelance.academyfreelanceproject"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProjectInvoice",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "status",
                    models.CharField(
                        choices=[("DUE", "Due"), ("APPROVED", "Approved"), ("IGNORED", "Ignored"), ("PAID", "Paid")],
                        default="DUE",
                        max_length=20,
                    ),
                ),
                ("total_duration_in_minutes", models.FloatField(default=0)),
                ("total_duration_in_hours", models.FloatField(default=0)),
                ("total_price", models.FloatField(default=0)),
                ("paid_at", models.DateTimeField(blank=True, default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "freelancer",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="freelance.freelancer"),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="freelance.freelanceprojectmember"
                    ),
                ),
                (
                    "reviewer",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
