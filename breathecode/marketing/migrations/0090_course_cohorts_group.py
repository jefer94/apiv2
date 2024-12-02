# Generated by Django 5.1.1 on 2024-10-21 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("admissions", "0064_academy_legal_name"),
        ("marketing", "0089_activecampaignacademy_crm_vendor"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="cohorts_group",
            field=models.ManyToManyField(
                blank=True,
                help_text="The student will be added to this cohorts when he buys the course",
                related_name="courses",
                to="admissions.cohort",
            ),
        ),
    ]
