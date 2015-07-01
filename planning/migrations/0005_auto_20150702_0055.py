# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0004_auto_20150701_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userplanning',
            name='secret_key',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]
