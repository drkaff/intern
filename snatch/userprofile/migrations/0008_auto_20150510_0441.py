# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0007_auto_20150510_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='job',
            name='skills',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
