# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150717_1533'),
    ]

    operations = [
        migrations.RenameField(
            model_name='label',
            old_name='url',
            new_name='website',
        ),
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nom'),
            preserve_default=True,
        ),
    ]
