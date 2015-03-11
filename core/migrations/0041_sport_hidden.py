# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20150311_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='sport',
            name='hidden',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
