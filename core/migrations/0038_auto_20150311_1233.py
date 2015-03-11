# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20150128_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='time',
            field=models.TimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='race',
            name='date',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
