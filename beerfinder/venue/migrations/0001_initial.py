# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('foursquare_id', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('street_address', models.CharField(max_length=100, blank=True)),
                ('city', models.CharField(max_length=100, blank=True)),
                ('state', models.CharField(max_length=100, blank=True)),
                ('postal_code', models.CharField(max_length=100, blank=True)),
                ('country', models.CharField(max_length=100, blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(help_text=b'(longitude, latitude) pairs', srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
