# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_usereducation'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercv',
            name='user_cv_education',
            field=models.IntegerField(default=0),
        ),
    ]
