# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Contact')),
                ('email', models.EmailField(max_length=75, blank=True, null=True)),
                ('phone', models.CharField(max_length=10, blank=True, null=True, verbose_name='Téléphone')),
            ],
            options={
            },
            bases=(core.models.ComparableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('website', models.URLField(blank=True, null=True, verbose_name='Site internet')),
                ('edition', models.PositiveSmallIntegerField(verbose_name="Numéro d'édition")),
                ('validated', models.BooleanField(default=False)),
                ('to_be_deleted', models.BooleanField(default=False)),
                ('event_mod_source', models.ForeignKey(to='events.Event', blank=True, null=True, related_name='event_modified_set')),
                ('event_prev_edition', models.OneToOneField(to='events.Event', blank=True, null=True, related_name='event_next_edition')),
            ],
            options={
            },
            bases=(core.models.ComparableModelMixin, models.Model),
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
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('street_number', models.CharField(max_length=10, blank=True, null=True, verbose_name='Numéro')),
                ('route', models.CharField(max_length=200, blank=True, null=True, verbose_name='Voie')),
                ('locality', models.CharField(max_length=100, verbose_name='Ville')),
                ('administrative_area_level_1', models.CharField(max_length=100, verbose_name='Région')),
                ('administrative_area_level_1_short_name', models.CharField(max_length=100)),
                ('administrative_area_level_2', models.CharField(max_length=100, verbose_name='Département')),
                ('administrative_area_level_2_short_name', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=16, verbose_name='Code Postal')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='Pays')),
                ('lat', models.DecimalField(max_digits=8, decimal_places=5)),
                ('lng', models.DecimalField(max_digits=8, decimal_places=5)),
                ('extra_info', models.TextField(blank=True, null=True, verbose_name='Infos complémentaires')),
            ],
            options={
            },
            bases=(core.models.ComparableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(blank=True, null=True)),
            ],
            options={
            },
            bases=(core.models.ComparableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, blank=True, null=True)),
                ('title', models.CharField(max_length=100, blank=True, null=True)),
                ('date', models.DateField()),
                ('time', models.TimeField(blank=True, null=True, verbose_name='Heure')),
                ('price', models.PositiveIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('to_be_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(max_length=100, blank=True, null=True)),
                ('import_source', models.CharField(max_length=100, blank=True, null=True)),
                ('import_source_id', models.CharField(max_length=100, blank=True, null=True)),
                ('contact', models.OneToOneField(to='events.Contact')),
                ('distance_cat', models.ForeignKey(to='core.DistanceCategory', verbose_name='Distance')),
                ('event', models.ForeignKey(to='events.Event', related_name='races')),
                ('federation', models.ForeignKey(to='core.Federation', blank=True, null=True, related_name='races')),
                ('label', models.ForeignKey(to='events.Label', blank=True, null=True, related_name='races')),
                ('location', models.OneToOneField(to='events.Location')),
                ('race_mod_source', models.ForeignKey(to='events.Race', blank=True, null=True, related_name='race_modified_set')),
                ('sport', models.ForeignKey(to='core.Sport')),
            ],
            options={
            },
            bases=(core.models.ComparableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StageDistanceSpecific',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField()),
                ('distance', models.PositiveIntegerField()),
                ('race', models.ForeignKey(to='events.Race', related_name='distances')),
                ('stage', models.ForeignKey(to='core.SportStage')),
            ],
            options={
                'verbose_name_plural': 'Stages distance (for a race)',
                'ordering': ['pk'],
                'verbose_name': 'Stage distance (for a race)',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(to='events.Organizer', blank=True, null=True),
            preserve_default=True,
        ),
    ]
