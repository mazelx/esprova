# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0002_auto_20150604_2254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='planning',
            old_name='planned_race',
            new_name='race',
        ),
        migrations.AddField(
            model_name='planning',
            name='registered',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
