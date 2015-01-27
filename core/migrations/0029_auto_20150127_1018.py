# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20150123_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(null=True, blank=True, to='core.Organizer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='race',
            name='federation',
            field=models.ForeignKey(related_name='races', null=True, blank=True, to='core.Federation'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='race',
            name='label',
            field=models.ForeignKey(related_name='races', null=True, blank=True, to='core.Label'),
            preserve_default=True,
        ),
    ]
