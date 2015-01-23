# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20150123_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='slug',
            field=models.SlugField(default='a', max_length=100),
            preserve_default=False,
        ),
    ]
