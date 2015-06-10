# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_auto_20150607_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='culture',
            field=models.CharField(default=datetime.datetime(2015, 6, 8, 0, 15, 59, 180684, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='quiz',
            field=models.CharField(default=datetime.datetime(2015, 6, 8, 0, 16, 6, 276383, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='culture',
            field=models.CharField(default=datetime.datetime(2015, 6, 8, 0, 16, 13, 926089, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='quiz',
            field=models.CharField(default=datetime.datetime(2015, 6, 8, 0, 16, 20, 908859, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
    ]
