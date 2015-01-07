# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20150106_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
