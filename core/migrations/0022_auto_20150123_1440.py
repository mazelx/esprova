# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20150122_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='slug',
            field=models.SlugField(null=True, blank=True, max_length=100),
            preserve_default=True,
        ),
    ]
