# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20150123_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='event',
            field=models.ForeignKey(related_name='races', to='core.Event'),
            preserve_default=True,
        ),
    ]
