# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='date',
            field=models.DateField(verbose_name='Date (ex. 2015-06-25)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='race',
            name='time',
            field=models.TimeField(blank=True, verbose_name='Heure (ex. 23:10)', null=True),
            preserve_default=True,
        ),
    ]
