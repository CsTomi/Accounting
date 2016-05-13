# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0004_auto_20160510_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportmaker',
            name='payer',
        ),
        migrations.AlterField(
            model_name='reportmaker',
            name='interval',
            field=jsonfield.fields.JSONField(default={}, help_text=b'Time interval, when the data collecting happened.', unique=True),
        ),
    ]
