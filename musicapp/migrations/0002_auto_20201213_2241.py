# Generated by Django 3.1.3 on 2020-12-13 22:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('musicapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(default=None, null=True, validators=[django.core.validators.MinValueValidator(13)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='band_exp',
            field=models.IntegerField(default=None, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterUniqueTogether(
            name='usergenre',
            unique_together={('user', 'genre')},
        ),
        migrations.AlterUniqueTogether(
            name='userinstrument',
            unique_together={('user', 'instrument')},
        ),
        migrations.AlterIndexTogether(
            name='usergenre',
            index_together={('user', 'genre')},
        ),
        migrations.AlterIndexTogether(
            name='userinstrument',
            index_together={('user', 'instrument')},
        ),
    ]
