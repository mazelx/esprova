# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20150119_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='administrative_area_level_1_short_name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='administrative_area_level_2_short_name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
