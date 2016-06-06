# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_auto_20160516_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aspects',
            name='filter',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='streams',
            name='bitrate',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='streams',
            name='password',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='streams',
            name='publish',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='streams',
            name='readonly',
            field=models.CharField(max_length=600),
        ),
        migrations.AlterField(
            model_name='streams',
            name='streamtype',
            field=models.CharField(max_length=100),
        ),
    ]
