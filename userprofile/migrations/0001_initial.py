# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import userprofile.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=100)),
                ('description', models.CharField(default=b'', max_length=200)),
                ('location', models.CharField(default=b'', max_length=100)),
                ('skills', models.CharField(default=b'', max_length=300)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('level', models.CharField(max_length=2, choices=[(b'in', b'Internship'), (b'en', b'Entry'), (b'ju', b'Junior'), (b'mi', b'Mid'), (b'se', b'Senior')])),
                ('job_type', models.CharField(max_length=2, choices=[(b'in', b'Internship'), (b'fl', b'Full Time'), (b'pt', b'Part Time'), (b'ct', b'Contract')])),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.CharField(default=b'', max_length=2, choices=[(b'em', b'Employer'), (b'ap', b'Applicant')])),
                ('skills', models.CharField(default=b'', max_length=300)),
                ('description', models.CharField(default=b'', max_length=300)),
                ('resume', models.FileField(null=True, upload_to=userprofile.models.upload_to_img)),
                ('profile_picture', models.ImageField(default=b'files/default.jpeg', upload_to=userprofile.models.upload_to_res)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
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
