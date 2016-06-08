# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='aspects',
            fields=[
                ('name', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('filter', models.CharField(max_length=2000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='customers',
            fields=[
                ('name', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('cpcode', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='streams',
            fields=[
                ('name', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('aspect', models.CharField(default=b'Not Found', max_length=100)),
                ('bitrate', models.CharField(default=b'Not Found', max_length=100)),
                ('streamtype', models.CharField(default=b'Not Found', max_length=100)),
                ('publish', models.CharField(default=b'Not Found', max_length=100)),
                ('password', models.CharField(default=b'Not Found', max_length=100)),
                ('readonly', models.CharField(default=b'Not Found', max_length=600)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
