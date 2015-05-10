# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0008_auto_20150510_0441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(default=b'', max_length=2, choices=[(b'em', b'Employer'), (b'ap', b'Applicant')]),
        ),
    ]
