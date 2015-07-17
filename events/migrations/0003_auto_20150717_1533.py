# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150717_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='url',
            field=models.URLField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='race',
            name='date',
            field=models.DateField(verbose_name='Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='race',
            name='time',
            field=models.TimeField(blank=True, null=True, verbose_name='Heure'),
            preserve_default=True,
        ),
    ]
