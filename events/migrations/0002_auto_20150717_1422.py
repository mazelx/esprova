# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='relay',
            field=models.BooleanField(default=False, verbose_name='Relais'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='race',
            name='timetrial',
            field=models.BooleanField(default=False, verbose_name='Contre-la-montre'),
            preserve_default=True,
        ),
    ]
