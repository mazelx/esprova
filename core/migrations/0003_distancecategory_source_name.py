# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150729_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='distancecategory',
            name='source_name',
            field=models.CharField(blank=True, max_length=20, null=True),
            preserve_default=True,
        ),
    ]
