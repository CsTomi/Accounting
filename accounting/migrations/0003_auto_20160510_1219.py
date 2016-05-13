# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_reportmaker_payer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportmaker',
            name='interval',
            field=jsonfield.fields.JSONField(default={}, help_text=b'Time interval, when the data collecting happened.'),
        ),
        migrations.AlterField(
            model_name='reportmaker',
            name='payer',
            field=models.CharField(max_length=50),
        ),
    ]
