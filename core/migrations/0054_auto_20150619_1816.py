# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_auto_20150619_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='import_source',
            field=models.CharField(blank=True, null=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='race',
            name='import_source_id',
            field=models.CharField(blank=True, null=True, max_length=100),
            preserve_default=True,
        ),
    ]
