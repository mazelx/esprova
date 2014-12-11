# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20141210_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='race',
            name='date',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
