# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-13 20:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VkModule', '0003_auto_20161113_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupinfo',
            name='group_name',
            field=models.TextField(default=models.CharField(max_length=100)),
        ),
    ]
