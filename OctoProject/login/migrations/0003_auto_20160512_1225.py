# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_quota'),
    ]

    operations = [
        migrations.CreateModel(
            name='aspects',
            fields=[
                ('name', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('filter', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='streams',
            name='bitrate',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='streams',
            name='password',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='streams',
            name='publish',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='streams',
            name='readonly',
            field=models.CharField(default=0, max_length=600),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='streams',
            name='streamtype',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
