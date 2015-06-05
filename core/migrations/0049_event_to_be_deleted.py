# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_auto_20150604_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='to_be_deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
