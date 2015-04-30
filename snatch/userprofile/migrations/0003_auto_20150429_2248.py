# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20150427_2347'),
    ]

    operations = [
        migrations.CreateModel(
            name='job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=None, max_length=100)),
                ('description', models.CharField(default=None, max_length=200)),
                ('location', models.CharField(default=None, max_length=100)),
                ('skills', models.CharField(default=None, max_length=300)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('level', models.CharField(max_length=2)),
                ('job_type', models.CharField(max_length=2)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='uType',
            field=models.CharField(max_length=2, choices=[(b'em', b'Employer'), (b'ap', b'Applicant')]),
        ),
        migrations.AddField(
            model_name='job',
            name='applied',
            field=models.ManyToManyField(related_name='applicants', to='userprofile.UserProfile'),
        ),
        migrations.AddField(
            model_name='job',
            name='company',
            field=models.ForeignKey(related_name='company', to='userprofile.UserProfile'),
        ),
    ]
