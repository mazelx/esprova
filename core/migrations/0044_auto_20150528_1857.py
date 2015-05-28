# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_remove_race_modified_source_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('website', models.URLField(blank=True, null=True)),
                ('edition', models.PositiveSmallIntegerField()),
                ('organizer', models.ForeignKey(null=True, blank=True, to='core.Organizer')),
                ('previous_edition', models.ForeignKey(null=True, blank=True, to='core.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='eventedition',
            name='event_ref',
        ),
        migrations.RemoveField(
            model_name='eventreference',
            name='organizer',
        ),
        migrations.DeleteModel(
            name='EventReference',
        ),
        migrations.AlterField(
            model_name='race',
            name='event',
            field=models.ForeignKey(to='core.Event', related_name='races'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='EventEdition',
        ),
    ]
