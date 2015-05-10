# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_auto_20150506_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='uType',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(default=datetime.datetime(2015, 5, 8, 22, 54, 10, 77566, tzinfo=utc), choices=[('em', 'Employer'), ('ap', 'Applicant')], max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='skills',
            field=models.CharField(default='', max_length=300),
        ),
    ]
