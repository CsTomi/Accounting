# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0005_auto_20160510_1223'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportmaker',
            options={'ordering': ['-interval'], 'get_latest_by': 'interval', 'verbose_name': 'report_makers', 'verbose_name_plural': 'report_maker'},
        ),
        migrations.AlterModelOptions(
            name='resourcecollector',
            options={'ordering': ['-interval'], 'get_latest_by': 'interval', 'verbose_name': 'resource_collectors', 'verbose_name_plural': 'resource_collector'},
        ),
    ]
