# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_sport_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='modified_source_id',
            field=models.ForeignKey(to='core.Race', null=True),
            preserve_default=True,
        ),
    ]
