# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='key',
            field=models.CharField(default='asm', unique=True, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
