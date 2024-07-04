# Generated by Django 3.2.12 on 2022-03-25 21:03

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("admissions", "0038_alter_cohort_syllabus_version"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Assessment",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("lang", models.CharField(blank=True, default="en", max_length=3)),
                (
                    "score_threshold",
                    models.IntegerField(
                        blank=True,
                        default=None,
                        help_text="You can set a threshold to determine if the user score is successfull",
                        null=True,
                    ),
                ),
                ("private", models.BooleanField(default=False)),
                ("comment", models.CharField(blank=True, default=None, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "academy",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text="Not all assesments are triggered by academies",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="admissions.academy",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "original",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text="The original translation (will only be set if the quiz is a translation of another one)",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="assessment.assessment",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("auth.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="UserAssessment",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(blank=True, max_length=200)),
                ("lang", models.CharField(blank=True, default="en", max_length=3)),
                ("total_score", models.FloatField(help_text="Total sum of all chosen options in the assesment")),
                ("opened", models.BooleanField(default=False)),
                (
                    "status",
                    models.CharField(
                        choices=[("DRAFT", "DRAFT"), ("SENT", "Sent"), ("EXPIRED", "Expired")],
                        default="DRAFT",
                        max_length=15,
                    ),
                ),
                ("comment", models.CharField(blank=True, default=None, max_length=255, null=True)),
                ("started_at", models.DateTimeField(blank=True, default=None, null=True)),
                ("finished_at", models.DateTimeField(blank=True, default=None, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "academy",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="admissions.academy",
                    ),
                ),
                (
                    "assessment",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="assessment.assessment",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.TextField()),
                ("help_text", models.CharField(blank=True, default=None, max_length=255, null=True)),
                ("lang", models.CharField(blank=True, default="en", max_length=3)),
                (
                    "question_type",
                    models.CharField(
                        choices=[
                            ("TEXT", "Text"),
                            ("NUMBER", "Number"),
                            ("SELECT", "Select"),
                            ("SELECT_MULTIPLE", "Select Multiple"),
                        ],
                        default="SELECT",
                        max_length=15,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "assessment",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="assessment.assessment",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Option",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.TextField()),
                ("help_text", models.CharField(blank=True, default=None, max_length=255, null=True)),
                ("lang", models.CharField(blank=True, default="en", max_length=3)),
                (
                    "score",
                    models.FloatField(
                        help_text="If picked, this value will add up to the total score of the assesment, you can have negative or fractional values"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "question",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="assessment.question",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "option",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text="Will be null if open question, no options to pick",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="assessment.option",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="assessment.question",
                    ),
                ),
                (
                    "user_assesment",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="assessment.userassessment",
                    ),
                ),
            ],
        ),
    ]
