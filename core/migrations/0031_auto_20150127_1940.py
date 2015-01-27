# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20150127_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='created_by',
            field=models.CharField(default='FFTri', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='race',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 27, 18, 40, 7, 863794, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='race',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 27, 18, 40, 15, 575972, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
