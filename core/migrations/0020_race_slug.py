# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_race_validated'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='slug',
            field=models.SlugField(default='a', max_length=100),
            preserve_default=False,
        ),
    ]
