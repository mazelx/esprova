# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20150127_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(null=True, blank=True, to='core.Organizer'),
            preserve_default=False,
        ),
    ]
