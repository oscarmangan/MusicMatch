# Generated by Django 3.1.3 on 2021-02-11 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0006_auto_20210208_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='facebook_url',
            field=models.URLField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='instagram_url',
            field=models.URLField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='twitter_url',
            field=models.URLField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
