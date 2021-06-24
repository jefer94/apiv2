# Generated by Django 3.1.3 on 2020-11-25 04:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0012_auto_20201124_1737'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketing', '0026_formentry_utm_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortLink',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('destination', models.URLField()),
                ('hits', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('destination_status',
                 models.CharField(choices=[('ACTIVE', 'Active'),
                                           ('NOT_FOUND', 'Not found')],
                                  default='ACTIVE',
                                  max_length=15)),
                ('utm_content',
                 models.CharField(blank=True,
                                  default=None,
                                  max_length=250,
                                  null=True)),
                ('utm_medium',
                 models.CharField(blank=True,
                                  default=None,
                                  max_length=50,
                                  null=True)),
                ('utm_campaign',
                 models.CharField(blank=True,
                                  default=None,
                                  max_length=50,
                                  null=True)),
                ('utm_source',
                 models.CharField(blank=True,
                                  default=None,
                                  max_length=50,
                                  null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academy',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='admissions.academy')),
                ('author',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
