# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20141217_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='latlng',
        ),
        migrations.AddField(
            model_name='location',
            name='lat',
            field=models.DecimalField(max_digits=8, decimal_places=5, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='lng',
            field=models.DecimalField(max_digits=8, decimal_places=5, default=1),
            preserve_default=False,
        ),
    ]
