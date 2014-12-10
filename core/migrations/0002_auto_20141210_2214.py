# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stagedistancedefault',
            options={'verbose_name': 'Stage distance (default)', 'verbose_name_plural': 'Stages distance (default)', 'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='stagedistancespecific',
            options={'verbose_name': 'Stage distance (for a race)', 'verbose_name_plural': 'Stages distance (for a race)', 'ordering': ['pk']},
        ),
    ]
