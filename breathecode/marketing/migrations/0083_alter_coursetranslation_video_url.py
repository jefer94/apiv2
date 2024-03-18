# Generated by Django 5.0.3 on 2024-03-18 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0082_course_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursetranslation',
            name='video_url',
            field=models.URLField(blank=True,
                                  default=None,
                                  help_text='Video that introduces/promotes this course',
                                  null=True),
        ),
    ]
