# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportMaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bills', jsonfield.fields.JSONField(default={}, help_text=b'Every users bill.')),
                ('start_date', models.DateTimeField(help_text=b'Begining of the accounting.')),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now, help_text=b'End of the accounting time intervall.')),
            ],
            options={
                'ordering': ['-start_date'],
                'db_table': 'acc_reportmaker',
                'verbose_name': 'report_makers',
                'verbose_name_plural': 'report_maker',
                'get_latest_by': 'start_date',
            },
        ),
        migrations.CreateModel(
            name='ResourceCollector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activities', jsonfield.fields.JSONField(default={}, help_text=b'Data about activities.')),
                ('start_date', models.DateTimeField(help_text=b'Begining of the accounting.')),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now, help_text=b'End of the accounting time intervall.')),
                ('is_collection_successfull', models.BooleanField(default=False, help_text=b'Is the resource and activity collection done?')),
                ('delta_time', models.IntegerField(default=0, help_text=b'The lenght of the accounting time interval in days.')),
            ],
            options={
                'ordering': ['-start_date'],
                'db_table': 'acc_resourcecollector',
                'verbose_name': 'resource_collectors',
                'verbose_name_plural': 'resource_collector',
                'get_latest_by': 'start_date',
            },
        ),
        migrations.AddField(
            model_name='reportmaker',
            name='collector',
            field=models.ForeignKey(to='accounting.ResourceCollector'),
        ),
    ]
