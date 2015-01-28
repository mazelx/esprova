# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20150128_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='end_date',
            field=models.DateField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='season',
            name='start_date',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
