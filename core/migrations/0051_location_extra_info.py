# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_race_to_be_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='extra_info',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
