# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20150119_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='validated',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
