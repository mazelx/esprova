# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_event_to_be_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='to_be_deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
