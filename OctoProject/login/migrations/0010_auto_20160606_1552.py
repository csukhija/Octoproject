# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_auto_20160606_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streams',
            name='aspect',
            field=models.CharField(default=b'Not Found', max_length=100),
        ),
        migrations.AlterField(
            model_name='streams',
            name='bitrate',
            field=models.CharField(default=b'Not Found', max_length=100),
        ),
        migrations.AlterField(
            model_name='streams',
            name='password',
            field=models.CharField(default=b'Not Found', max_length=100),
        ),
        migrations.AlterField(
            model_name='streams',
            name='publish',
            field=models.CharField(default=b'Not Found', max_length=100),
        ),
        migrations.AlterField(
            model_name='streams',
            name='readonly',
            field=models.CharField(default=b'Not Found', max_length=600),
        ),
        migrations.AlterField(
            model_name='streams',
            name='streamtype',
            field=models.CharField(default=b'Not Found', max_length=100),
        ),
    ]
