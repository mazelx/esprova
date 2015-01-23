# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20150123_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='slug',
            field=models.SlugField(blank=True, null=True, max_length=100),
            preserve_default=True,
        ),
    ]
