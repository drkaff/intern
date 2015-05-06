# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0003_auto_20150429_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='skills',
            field=models.CharField(default=b'', max_length=300),
        ),
    ]
