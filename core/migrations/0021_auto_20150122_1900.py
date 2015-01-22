# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_race_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stagedistancespecific',
            name='race',
            field=models.ForeignKey(to='core.Race', related_name='distances'),
            preserve_default=True,
        ),
    ]
