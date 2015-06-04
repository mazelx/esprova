# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_auto_20150529_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='race_mod_source',
            field=models.ForeignKey(blank=True, related_name='race_modified_set', null=True, to='core.Race'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Contact'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Téléphone'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='edition',
            field=models.PositiveSmallIntegerField(verbose_name="Numéro d'édition"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='website',
            field=models.URLField(blank=True, null=True, verbose_name='Site internet'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='administrative_area_level_1',
            field=models.CharField(max_length=100, verbose_name='Région'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='administrative_area_level_2',
            field=models.CharField(max_length=100, verbose_name='Département'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, verbose_name='Pays'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='locality',
            field=models.CharField(max_length=100, verbose_name='Ville'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='postal_code',
            field=models.CharField(max_length=16, verbose_name='Code Postal'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='route',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Voie'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='street_number',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Numéro'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='race',
            name='contact',
            field=models.OneToOneField(to='core.Contact'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='race',
            name='distance_cat',
            field=models.ForeignKey(verbose_name='Distance', to='core.DistanceCategory'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='race',
            name='time',
            field=models.TimeField(blank=True, null=True, verbose_name='Heure'),
            preserve_default=True,
        ),
    ]
