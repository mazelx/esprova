# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20150128_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='name',
        ),
        migrations.RemoveField(
            model_name='event',
            name='organizer',
        ),
        migrations.RemoveField(
            model_name='event',
            name='website',
        ),
    ]
