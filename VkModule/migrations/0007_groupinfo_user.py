# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-24 16:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('VkModule', '0006_auto_20170217_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupinfo',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
