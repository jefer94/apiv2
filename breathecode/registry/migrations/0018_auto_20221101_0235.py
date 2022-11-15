# Generated by Django 3.2.16 on 2022-11-01 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0017_merge_20221031_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetcategory',
            name='auto_generate_previews',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='assetcategory',
            name='preview_generation_url',
            field=models.URLField(blank=True,
                                  default=None,
                                  help_text='Will be POSTed to get preview image',
                                  null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='technologies',
            field=models.ManyToManyField(blank=True, to='registry.AssetTechnology'),
        ),
    ]