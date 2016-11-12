# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('VkModule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='changegroup',
            name='date',
            field=models.DateField(default=datetime.date(2016, 11, 12)),
        ),
    ]
