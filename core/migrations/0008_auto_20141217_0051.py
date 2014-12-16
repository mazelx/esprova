# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20141217_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
            preserve_default=True,
        ),
    ]
