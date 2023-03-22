# Generated by Django 3.2.16 on 2023-03-17 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0055_cohort_available_as_saas'),
    ]

    operations = [
        migrations.AddField(
            model_name='cohort',
            name='accepts_enrollment_suggestions',
            field=models.BooleanField(
                default=True, help_text='The system will suggest won leads to be added to this cohort'),
        ),
        migrations.AlterField(
            model_name='cohort',
            name='private',
            field=models.BooleanField(
                default=False,
                help_text=
                'It will not show on the public API endpoints but you will still be able to add people manually'
            ),
        ),
    ]