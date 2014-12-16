# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20141215_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('address', models.CharField(max_length=200, blank=True, null=True)),
                ('zipcode', models.CharField(max_length=16, blank=True, null=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100, blank=True, null=True)),
                ('lat', models.DecimalField(max_digits=7, decimal_places=5)),
                ('lng', models.DecimalField(max_digits=7, decimal_places=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='race',
            name='location',
            field=models.OneToOneField(to='core.Location', default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='race',
            name='price',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
