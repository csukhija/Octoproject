# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_auto_20160512_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streams',
            name='password',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='streams',
            name='publish',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='streams',
            name='readonly',
            field=models.CharField(default=b'', max_length=600),
        ),
    ]
