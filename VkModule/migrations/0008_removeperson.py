# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-30 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VkModule', '0007_groupinfo_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemovePerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remove_person', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'remove_persons',
            },
        ),
    ]