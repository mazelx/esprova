# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20141216_2359'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='address',
            new_name='address1',
        ),
        migrations.RemoveField(
            model_name='location',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='location',
            name='lng',
        ),
        migrations.AddField(
            model_name='location',
            name='address2',
            field=models.CharField(null=True, max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='country',
            field=models.CharField(max_length=100, default='France'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='latlng',
            field=models.CharField(max_length=100, default=(1, 1), blank=True),
            preserve_default=False,
        ),
    ]
