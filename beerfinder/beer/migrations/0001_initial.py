# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=75)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=150)),
                ('normalized_name', models.CharField(help_text=b'normalized, simplified name for easy searching', max_length=75, db_index=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Brewery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=75)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=75)),
                ('normalized_name', models.CharField(help_text=b'normalized, simplified name for easy searching', max_length=75, db_index=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServingType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=25)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(max_length=25, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='beer',
            name='brewery',
            field=models.ForeignKey(to='beer.Brewery'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beer',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beer',
            name='style',
            field=models.ForeignKey(blank=True, to='beer.Style', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='beer',
            unique_together=set([('name', 'brewery')]),
        ),
    ]
