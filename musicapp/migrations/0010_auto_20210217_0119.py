# Generated by Django 3.1.3 on 2021-02-17 01:19

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0009_auto_20210216_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='lat_long',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, default=None, null=True, srid=4326),
        ),
    ]
