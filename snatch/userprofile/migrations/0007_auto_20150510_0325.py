# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_auto_20150508_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(choices=[('in', 'Internship'), ('fl', 'Full Time'), ('pt', 'Part Time'), ('ct', 'Contract')], max_length=2),
        ),
        migrations.AlterField(
            model_name='job',
            name='level',
            field=models.CharField(choices=[('in', 'Internship'), ('en', 'Entry'), ('ju', 'Junior'), ('mi', 'Mid'), ('se', 'Senior')], max_length=2),
        ),
    ]
