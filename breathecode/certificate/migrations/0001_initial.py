# Generated by Django 3.1 on 2020-09-07 23:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admissions', '0008_auto_20200708_0049'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('logo_url',
                 models.CharField(blank=True,
                                  default=None,
                                  max_length=250,
                                  null=True)),
                ('duration_in_hours',
                 models.IntegerField(blank=True, default=None, null=True)),
                ('expiration_day_delta',
                 models.IntegerField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSpecialty',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('token',
                 models.CharField(db_index=True, max_length=40, unique=True)),
                ('expires_at',
                 models.DateTimeField(blank=True, default=None, null=True)),
                ('academy',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='admissions.academy')),
                ('specialty',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='certificate.specialty')),
                ('user',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id',
                 models.AutoField(auto_created=True,
                                  primary_key=True,
                                  serialize=False,
                                  verbose_name='ID')),
                ('slug', models.SlugField(max_length=150, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('logo_url',
                 models.CharField(blank=True,
                                  default=None,
                                  max_length=250,
                                  null=True)),
                ('duration_in_hours', models.IntegerField()),
                ('expiration_day_delta',
                 models.IntegerField(blank=True, default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('specialties',
                 models.ManyToManyField(to='certificate.Specialty')),
            ],
        ),
    ]
