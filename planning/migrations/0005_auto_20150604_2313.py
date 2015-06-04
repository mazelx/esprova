# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0004_auto_20150604_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortlistedrace',
            name='registered',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='shortlistedrace',
            unique_together=set([('user', 'race')]),
        ),
    ]
