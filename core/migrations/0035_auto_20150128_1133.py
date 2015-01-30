# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20150128_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_master',
            field=models.ForeignKey(default=1, to='core.EventMaster'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='season',
            field=models.ForeignKey(default=1, to='core.Season'),
            preserve_default=False,
        ),
    ]
