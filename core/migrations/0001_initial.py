# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DistanceCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=2)),
                ('long_name', models.CharField(max_length=20, blank=True, null=True)),
                ('order', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name_plural': 'Distance Categories',
                'verbose_name': 'Distance Category',
            },
            bases=(core.models.ComparableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Federation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('combinedSport', models.BooleanField(default=False)),
                ('hidden', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(core.models.ComparableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SportStage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('default_order', models.PositiveSmallIntegerField()),
                ('sport', models.ForeignKey(to='core.Sport')),
            ],
            options={
                'verbose_name_plural': 'Sport Stages',
                'ordering': ['sport', 'default_order'],
                'verbose_name': 'Sport Stage',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StageDistanceDefault',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField()),
                ('distance', models.PositiveIntegerField()),
                ('distance_cat', models.ForeignKey(to='core.DistanceCategory')),
                ('stage', models.ForeignKey(to='core.SportStage')),
            ],
            options={
                'verbose_name_plural': 'Stages distance (default)',
                'ordering': ['pk'],
                'verbose_name': 'Stage distance (default)',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='federation',
            name='sport',
            field=models.ManyToManyField(to='core.Sport'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='distancecategory',
            name='sport',
            field=models.ForeignKey(to='core.Sport'),
            preserve_default=True,
        ),
    ]
