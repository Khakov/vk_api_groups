# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delete_persons', models.TextField()),
                ('new_persons', models.TextField()),
            ],
            options={
                'db_table': 'changes',
            },
        ),
        migrations.CreateModel(
            name='GroupInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_id', models.CharField(max_length=100)),
                ('users', models.TextField()),
            ],
            options={
                'db_table': 'groups',
            },
        ),
        migrations.AddField(
            model_name='changegroup',
            name='group',
            field=models.ForeignKey(to='VkModule.GroupInfo'),
        ),
    ]
