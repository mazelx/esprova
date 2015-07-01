# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planning', '0002_auto_20150701_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPlanning',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('secret_key', models.CharField(max_length=40)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='shortlistedrace',
            name='user',
        ),
        migrations.AddField(
            model_name='shortlistedrace',
            name='user_planning',
            field=models.ForeignKey(related_name='races', null=True, to='planning.UserPlanning'),
            preserve_default=True,
        ),
    ]
