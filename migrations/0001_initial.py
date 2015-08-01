# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('time', models.DateTimeField()),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('original_time', models.DateTimeField()),
                ('url', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('hidden', models.BooleanField(default=False)),
                ('canceled', models.BooleanField(default=False)),
                ('flags', models.CharField(blank=True, max_length=255)),
                ('categories', models.CharField(blank=True, max_length=255)),
                ('order', models.FloatField(default=0.0)),
                ('cancel_reason', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'ordering': ['time', 'name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='location',
            name='schedule',
            field=models.ForeignKey(to='schedule.Schedule'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(to='schedule.Location'),
            preserve_default=True,
        ),
    ]
