# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0003_auto_20150701_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortlistedrace',
            name='user_planning',
            field=models.ForeignKey(to='planning.UserPlanning', related_name='races', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userplanning',
            name='user',
            field=models.ForeignKey(unique=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
