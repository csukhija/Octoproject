# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20160512_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streams',
            name='streamtype',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
