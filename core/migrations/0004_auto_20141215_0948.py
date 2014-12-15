# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20141211_1134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='distancecategory',
            options={'verbose_name_plural': 'Distance Categories', 'verbose_name': 'Distance Category'},
        ),
    ]
