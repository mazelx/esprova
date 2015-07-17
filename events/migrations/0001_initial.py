# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='Contact', max_length=100)),
                ('email', models.EmailField(null=True, max_length=75, blank=True)),
                ('phone', models.CharField(null=True, verbose_name='Téléphone', max_length=10, blank=True)),
            ],
            options={
            },
            bases=(core.models.ComparableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name="Nom de l'événement", max_length=150)),
                ('website', models.URLField(null=True, verbose_name='Site internet', blank=True)),
                ('edition', models.PositiveSmallIntegerField(verbose_name="Numéro d'édition")),
                ('validated', models.BooleanField(default=False)),
                ('to_be_deleted', models.BooleanField(default=False)),
                ('event_mod_source', models.ForeignKey(null=True, to='events.Event', blank=True, related_name='event_modified_set')),
                ('event_prev_edition', models.OneToOneField(null=True, to='events.Event', related_name='event_next_edition', blank=True)),
            ],
            options={
            },
            bases=(core.models.ComparableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('street_number', models.CharField(null=True, verbose_name='Numéro', max_length=10, blank=True)),
                ('route', models.CharField(null=True, verbose_name='Voie', max_length=200, blank=True)),
                ('locality', models.CharField(verbose_name='Ville', max_length=100)),
                ('administrative_area_level_1', models.CharField(verbose_name='Région', max_length=100)),
                ('administrative_area_level_1_short_name', models.CharField(max_length=100)),
                ('administrative_area_level_2', models.CharField(verbose_name='Département', max_length=100)),
                ('administrative_area_level_2_short_name', models.CharField(max_length=100)),
                ('postal_code', models.CharField(verbose_name='Code Postal', max_length=16)),
                ('country', django_countries.fields.CountryField(verbose_name='Pays', max_length=2)),
                ('lat', models.DecimalField(decimal_places=5, max_digits=8)),
                ('lng', models.DecimalField(decimal_places=5, max_digits=8)),
                ('extra_info', models.TextField(null=True, verbose_name='Infos complémentaires', blank=True)),
            ],
            options={
            },
            bases=(core.models.ComparableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(null=True, blank=True)),
            ],
            options={
            },
            bases=(core.models.ComparableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('slug', models.SlugField(null=True, max_length=100, blank=True)),
                ('title', models.CharField(null=True, max_length=100, blank=True)),
                ('date', models.DateField(verbose_name='Date (ex. 2015-06-25)')),
                ('time', models.TimeField(null=True, verbose_name='Heure (ex. 23:10)', blank=True)),
                ('price', models.PositiveIntegerField(null=True, blank=True)),
                ('description', models.TextField(null=True, verbose_name='Description de la course', blank=True)),
                ('to_be_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('modified_by', models.CharField(null=True, max_length=100, blank=True)),
                ('import_source', models.CharField(null=True, max_length=100, blank=True)),
                ('import_source_id', models.CharField(null=True, max_length=100, blank=True)),
                ('contact', models.OneToOneField(to='events.Contact')),
                ('distance_cat', models.ForeignKey(to='core.DistanceCategory', verbose_name='Distance')),
                ('event', models.ForeignKey(to='events.Event', related_name='races')),
                ('federation', models.ForeignKey(null=True, to='core.Federation', blank=True, related_name='races')),
                ('label', models.ForeignKey(null=True, to='events.Label', blank=True, related_name='races')),
                ('location', models.OneToOneField(to='events.Location')),
                ('race_mod_source', models.ForeignKey(null=True, to='events.Race', blank=True, related_name='race_modified_set')),
                ('sport', models.ForeignKey(to='core.Sport')),
            ],
            options={
            },
            bases=(core.models.ComparableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StageDistanceSpecific',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('order', models.PositiveSmallIntegerField()),
                ('distance', models.PositiveIntegerField()),
                ('race', models.ForeignKey(to='events.Race', related_name='distances')),
                ('stage', models.ForeignKey(to='core.SportStage')),
            ],
            options={
                'verbose_name_plural': 'Stages distance (for a race)',
                'verbose_name': 'Stage distance (for a race)',
                'ordering': ['pk'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(null=True, to='events.Organizer', blank=True, verbose_name='Organisateur'),
            preserve_default=True,
        ),
    ]
