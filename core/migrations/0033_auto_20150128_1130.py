# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20150128_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='name',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
