# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DistanceCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=2)),
                ('long_name', models.CharField(blank=True, null=True, max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntryFee',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('from_date', models.DateField(null=True)),
                ('to_date', models.DateField(null=True)),
                ('Price', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
            options={
            },
            bases=(models.Model,),
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
            name='Label',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, null=True, max_length=100)),
                ('edition', models.PositiveSmallIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('price', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('contact', models.ForeignKey(to='core.Contact')),
                ('distance_cat', models.ForeignKey(to='core.DistanceCategory')),
                ('event', models.ForeignKey(to='core.Event')),
                ('federation', models.ForeignKey(to='core.Federation', blank=True, null=True)),
                ('label', models.ForeignKey(to='core.Label', blank=True, null=True)),
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
            ],
            options={
            },
            bases=(models.Model,),
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
                'ordering': ['sport', 'default_order'],
                'verbose_name_plural': 'Sport Stages',
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
                'ordering': ['pk'],
                'verbose_name_plural': 'Stages distance (default for a distance category)',
                'verbose_name': 'Stage distance (default for a distance category)',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StageDistanceSpecific',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField()),
                ('distance', models.PositiveIntegerField()),
                ('race', models.ForeignKey(to='core.Race')),
                ('stage', models.ForeignKey(to='core.SportStage')),
            ],
            options={
                'ordering': ['pk'],
                'verbose_name_plural': 'Stages distance (specific for a race)',
                'verbose_name': 'Stage distance (specific for a race)',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='race',
            name='sport',
            field=models.ForeignKey(to='core.Sport'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='federation',
            name='sport',
            field=models.ManyToManyField(to='core.Sport'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entryfee',
            name='race',
            field=models.ForeignKey(to='core.Race'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='distancecategory',
            name='sport',
            field=models.ForeignKey(to='core.Sport'),
            preserve_default=True,
        ),
    ]
