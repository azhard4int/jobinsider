# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_title', models.CharField(max_length=255, blank=True)),
                ('user_overview', models.TextField(blank=True)),
                ('user_bio_status', models.BooleanField(default=0)),
                ('user_portrait', models.ImageField(upload_to=b'/home/azhar/Python/fyp/jobinsider/jobsinsider_app/media/userprofile/')),
                ('user_language_pre', models.IntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_cv_title', models.CharField(max_length=255, blank=True)),
                ('user_cv_file', models.FileField(upload_to=b'/home/azhar/Python/fyp/jobinsider/jobsinsider_app/media/users/cv/%Y/%m/%d')),
                ('user_cv_builder_status', models.BooleanField(default=0)),
                ('user_cv_review_status', models.IntegerField(default=0)),
                ('user_cv_builder', models.IntegerField(default=0)),
                ('user_cv_emp_status', models.BooleanField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserEmployment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=255, blank=True)),
                ('company_location', models.CharField(max_length=255, blank=True)),
                ('company_worktitle', models.CharField(max_length=255, blank=True)),
                ('company_role', models.CharField(max_length=255, blank=True)),
                ('company_from', models.DateField(blank=True)),
                ('company_to', models.DateField(blank=True)),
                ('company_description', models.TextField(blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_address', models.TextField(max_length=255, blank=True)),
                ('user_city', models.CharField(max_length=255, blank=True)),
                ('user_country', models.CharField(max_length=255, blank=True)),
                ('user_zipcode', models.CharField(max_length=255, blank=True)),
                ('user_phone_no', models.CharField(max_length=255, blank=True)),
                ('user_location_status', models.BooleanField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSkills',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('skills', models.CharField(max_length=255, blank=True)),
                ('skill_status', models.BooleanField(default=0)),
                ('category', models.ForeignKey(to='core.Categories')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
