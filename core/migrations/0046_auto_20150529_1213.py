# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_remove_race_validated'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='mod_source_event',
            field=models.ForeignKey(to='core.Event', blank=True, related_name='event_modified_set', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='validated',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='previous_edition',
            field=models.OneToOneField(null=True, blank=True, to='core.Event', related_name='event_next_edition'),
            preserve_default=True,
        ),
    ]
