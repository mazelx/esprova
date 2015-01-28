# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20150128_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventEdition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('edition', models.PositiveSmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='EventMaster',
            new_name='EventReference',
        ),
        migrations.RemoveField(
            model_name='event',
            name='event_master',
        ),
        migrations.RemoveField(
            model_name='event',
            name='season',
        ),
        migrations.AddField(
            model_name='eventedition',
            name='event_ref',
            field=models.ForeignKey(to='core.EventReference'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='race',
            name='event',
            field=models.ForeignKey(to='core.EventEdition', related_name='races'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
