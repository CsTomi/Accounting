# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0006_auto_20160510_1235'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportmaker',
            options={'ordering': ['-start_date'], 'get_latest_by': 'start_date', 'verbose_name': 'report_makers', 'verbose_name_plural': 'report_maker'},
        ),
        migrations.AlterModelOptions(
            name='resourcecollector',
            options={'ordering': ['-start_date'], 'get_latest_by': 'start_date', 'verbose_name': 'resource_collectors', 'verbose_name_plural': 'resource_collector'},
        ),
        migrations.RemoveField(
            model_name='reportmaker',
            name='interval',
        ),
        migrations.RemoveField(
            model_name='resourcecollector',
            name='interval',
        ),
        migrations.AddField(
            model_name='reportmaker',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text=b'End of the accounting time intervall.'),
        ),
        migrations.AddField(
            model_name='reportmaker',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 19, 54, 15, 836905, tzinfo=utc), help_text=b'Begining of the accounting.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resourcecollector',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text=b'End of the accounting time intervall.'),
        ),
        migrations.AddField(
            model_name='resourcecollector',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 10, 19, 54, 30, 328582, tzinfo=utc), help_text=b'Begining of the accounting.'),
            preserve_default=False,
        ),
    ]
