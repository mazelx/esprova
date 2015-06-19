# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0052_auto_20150619_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='modified_by',
            field=models.CharField(null=True, blank=True, max_length=100),
            preserve_default=True,
        ),
    ]
