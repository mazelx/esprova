# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20150119_1221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='street_address',
            new_name='street_number',
        ),
    ]
