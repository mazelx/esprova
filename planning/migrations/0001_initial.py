# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        # migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        # ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortlistedRace',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('registered', models.BooleanField(default=False)),
                ('race', models.ForeignKey(to='events.Race')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='shortlistedrace',
            unique_together=set([('user', 'race')]),
        ),
    ]
