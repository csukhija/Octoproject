# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20160512_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streams',
            name='bitrate',
            field=models.CharField(default=b'x', max_length=100),
        ),
    ]
