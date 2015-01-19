# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_distancecategory_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='city',
            new_name='locality',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='address1',
            new_name='route',
        ),
        migrations.RemoveField(
            model_name='location',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='location',
            name='state',
        ),
        migrations.RemoveField(
            model_name='location',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='location',
            name='administrative_area_level_1',
            field=models.CharField(default='Rhône-Alpes', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='administrative_area_level_1_short_name',
            field=models.CharField(default='RA', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='administrative_area_level_2',
            field=models.CharField(default='Ardèche', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='administrative_area_level_2_short_name',
            field=models.CharField(default='07', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='postal_code',
            field=models.CharField(default='07400', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='street_address',
            field=models.CharField(blank=True, null=True, max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.DecimalField(max_digits=8, decimal_places=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='lng',
            field=models.DecimalField(max_digits=8, decimal_places=5),
            preserve_default=True,
        ),
    ]
