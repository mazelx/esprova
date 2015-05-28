# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_race_modified_source_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='modified_source_id',
        ),
    ]
