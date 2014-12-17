# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20141217_0051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='edition',
        ),
        migrations.AddField(
            model_name='event',
            name='edition',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
