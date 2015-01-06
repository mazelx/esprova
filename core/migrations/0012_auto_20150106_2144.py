# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150106_2101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entryfee',
            name='race',
        ),
        migrations.DeleteModel(
            name='EntryFee',
        ),
        migrations.AddField(
            model_name='event',
            name='website',
            field=models.URLField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
