# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0003_auto_20150604_2307'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Planning',
            new_name='ShortListedRace',
        ),
    ]
