# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20160512_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streams',
            name='bitrate',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
