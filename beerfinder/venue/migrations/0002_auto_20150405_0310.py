# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
