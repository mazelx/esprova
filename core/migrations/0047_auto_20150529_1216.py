# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_auto_20150529_1213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='mod_source_event',
            new_name='event_mod_source',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='previous_edition',
            new_name='event_prev_edition',
        ),
    ]
