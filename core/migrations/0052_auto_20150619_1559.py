# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_location_extra_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='modified_by',
            field=models.CharField(max_length=100, default='fftri'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='extra_info',
            field=models.TextField(blank=True, verbose_name='Infos complémentaires', null=True),
            preserve_default=True,
        ),
    ]
