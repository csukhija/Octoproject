# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_auto_20160512_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streams',
            name='readonly',
            field=models.CharField(default=b'', max_length=2000),
        ),
    ]
