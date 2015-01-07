# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150106_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='email',
            field=models.EmailField(null=True, max_length=75, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='phone',
            field=models.CharField(null=True, max_length=10, blank=True),
            preserve_default=True,
        ),
    ]
