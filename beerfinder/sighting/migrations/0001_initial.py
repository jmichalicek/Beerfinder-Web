# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('beer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('text', models.TextField()),
            ],
            options={
                'ordering': ('-date_created', 'sighting'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sighting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_sighted', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('comment', models.TextField(blank=True)),
                ('beer', models.ForeignKey(to='beer.Beer')),
                ('serving_types', models.ManyToManyField(help_text=b'How was the beer available', to='beer.ServingType', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
                ('venue', models.ForeignKey(to='venue.Venue')),
            ],
            options={
                'ordering': ('-date_sighted', 'beer', 'venue__name'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SightingConfirmation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_available', models.BooleanField(default=False, db_index=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('sighting', models.ForeignKey(to='sighting.Sighting')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ('-date_created', 'sighting'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SightingImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('original', models.ImageField(height_field=b'original_height', width_field=b'original_width', max_length=250, upload_to=b'sighting_images/%Y/%m/%d')),
                ('original_height', models.IntegerField(null=True, blank=True)),
                ('original_width', models.IntegerField(null=True, blank=True)),
                ('thumbnail', models.ImageField(default=b'', max_length=250, upload_to=b'sighting/images/%Y/%m/%d', blank=True)),
                ('thumbnail_height', models.IntegerField(null=True, blank=True)),
                ('thumbnail_width', models.IntegerField(null=True, blank=True)),
                ('small', models.ImageField(default=b'', max_length=250, upload_to=b'sighting/images/%Y/%m/%d', blank=True)),
                ('small_height', models.IntegerField(null=True, blank=True)),
                ('small_width', models.IntegerField(null=True, blank=True)),
                ('medium', models.ImageField(default=b'', max_length=250, upload_to=b'sighting/images/%Y/%m/%d', blank=True)),
                ('medium_height', models.IntegerField(null=True, blank=True)),
                ('medium_width', models.IntegerField(null=True, blank=True)),
                ('sighting', models.ForeignKey(related_name=b'sighting_images', to='sighting.Sighting')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comment',
            name='sighting',
            field=models.ForeignKey(related_name=b'comments', to='sighting.Sighting'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
