#!/usr/env/bin python
# coding=utf-8
# vim: set fileencoding=utf-8

###########################################################
#
# Accounting - You are ALL gonna pay...
#
#
#
#
############################################################

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models import (BooleanField, IntegerField,
                    ForeignKey, DateTimeField, DecimalField)

from datetime import datetime
from datetime import timedelta
from django.utils import timezone

from operator import itemgetter

import json
from jsonfield import JSONField

ACC_DATE_FORMAT = '%Y.%m.%d %H:%M:%S.%f'  # const to the dates
ACC_OUT_FILE = 'acc_out.txt'


class ResourceCollector(models.Model):
    # Every important data for a bill
    activities = JSONField(null=False, default={},
                           help_text='Data about activities.')

    start_date = DateTimeField(null=False,
                            help_text='Begining of the accounting.')
                            
    end_date = DateTimeField(null=False, default=timezone.now,
                            help_text='End of the accounting'+
                            ' time intervall.')

    is_collection_successfull = BooleanField(null=False, default=False,
                                             help_text='Is the resource' +
                                             ' and activity collection' +
                                             ' done?')

    delta_time = IntegerField(null=False, default=0,
                              help_text='The lenght of the accounting' +
                              ' time interval in days.')

    @classmethod
    def create(cls, dt=7, activities={}):
        temp_date = datetime.now()

        # when it's called, but end of that day
        finish = datetime(temp_date.year,
                            temp_date.month,
                            temp_date.day,
                            temp_date.hour + (23 - temp_date.hour),
                            temp_date.minute + (59 - temp_date.minute),
                            temp_date.second + (59 - temp_date.second))

        # begining of the accounting intervall
        start = finish - timedelta(
                                    days=dt,
                                    hours=finish.hour,
                                    minutes=finish.minute,
                                    seconds=finish.second)
        print start

        is_ok = True
        if activities.keys() is None:
            is_ok = False

        acc = cls(start_date=start,
                end_date=finish,
                activities=activities,
                is_collection_successfull=is_ok,
                delta_time=dt)
        acc.save()
        return acc

    class Meta:
        app_label = 'accounting'
        db_table = 'acc_resourcecollector'
        verbose_name = ('resource_collectors')
        verbose_name_plural = ('resource_collector')
        ordering = ['-start_date']
        get_latest_by = 'start_date'

    def __str__(self):
        return u'Resource_Collector'

    # Collect data.
    def collect_data(self):
        try:
            # get every user from the db
            users = User.objects.all()

            for user in users:
                temp_list = []

                for act in user.instanceactivity_set.filter(
                        Q(started__range=(self.start_date,
                                          self.end_date)),
                        Q(finished__range=(self.start_date,
                                        self.end_date)),
                        Q(succeeded__exact=True),
                        Q(activity_code__exact='vm.Instance.deploy') |
                        Q(activity_code__exact='vm.Instance.create') |
                        Q(activity_code__exact='vm.Instance.destroy') |
                        Q(activity_code__exact='vm.Instance.sleep') |
                        Q(activity_code__exact='vm.Instance.wake_up') |
                        Q(activity_code__exact='vm.Instance.sleep') |
                        Q(activity_code__exact='vm.Instance.renew') |
                        Q(activity_code__exact='vm.Instance.shut_off')
                        ).order_by('instance_id', 'started').values(
                        'id', 'instance_id', 'user_id', 'started',
                        'finished', 'activity_code'):

                    useful_data_chunk = dict(
                        id=act['id'],  # Activity ID
                        activity_code=act['activity_code'],  # What?
                        started=act['started'].strftime(
                            ACC_DATE_FORMAT),  # When did it started?
                        finished=act['finished'].strftime(
                            ACC_DATE_FORMAT),  # When did it finished?
                        user_id=act['user_id'],  # Who did that?
                        instance_id=act['instance_id'])  # Which machine

                    temp_data = self.get_instance_data(user, act['instance_id'])
                    useful_data_chunk.update(temp_data)

                    temp_list.append(useful_data_chunk)

                self.activities[user.get_username()] = temp_list

            self.is_collection_successfull = True
            return True
        except OSError as ex:
            return False
            
    def get_instance_data(self, user, ins_id):
        data = dict()
        # Usage of the vm's
        # Every column
        instances = user.instance_set.filter(
            Q(id__exact=ins_id)).all()

        if len(instances) == 1:
            ins = instances[0]
            # Get all disks
            disks_ = ins.disks.all().values('size')
            
            # ha nem a user csinálta, akkor a mások csinálta, csak az a kérdés, hogy ki
            owners = ins.get_users_with_level()
            owner_list = []
            
            for owner in owners:
                usr = owner[0].get_username()
                if not usr == user.get_username():
                    owner_list.append(usr)
            
            data['other_owners'] = owner_list            
            data['ram'] = ins.ram_size
            data['cores'] = ins.num_cores
            data['core_prio'] = ins.priority
            data['disks'] = []

            for disk in disks_:
                data['disks'].append(disk)
        else:
            # Sharaed machine
            data['ram'] = -1
            data['cores'] = -1
            data['core_prio'] = -1
            data['disks'] = []
                       
        return data
        
    @classmethod
    def collect_user_data(self, start_time, end_time, user_name):
        if str(type(start_time)) == '<type \'str\'>':
            start_date = datetime.strpdate(start_time, ACC_DATE_FORMAT)

        if str(type(end_time)) == '<type \'str\'>':
            end_date = datetime.strpdate(end_time, ACC_DATE_FORMAT)

        if (str(type(start_time)) == '<type \'datetime.datetime\'>' and
                str(type(end_time)) == '<type \'datetime.datetime\'>'):
            start = start_time
            end = end_time
        else:
            return None

        user = User.objects.filter(username__exact=user_name).all()
        if user is None:
            return None

        user = user[0]
        temp_list = []
        usr_acts = user.instanceactivity_set.filter(
                        Q(started__range=(start, end)),
                        Q(finished__range=(start, end)),
                        Q(succeeded__exact=True),
                        Q(activity_code__exact='vm.Instance.deploy') |
                        Q(activity_code__exact='vm.Instance.create') |
                        Q(activity_code__exact='vm.Instance.destroy') |
                        Q(activity_code__exact='vm.Instance.sleep') |
                        Q(activity_code__exact='vm.Instance.wake_up') |
                        Q(activity_code__exact='vm.Instance.sleep') |
                        Q(activity_code__exact='vm.Instance.renew') |
                        Q(activity_code__exact='vm.Instance.shut_off')
                        ).order_by('instance_id', 'started').values(
                            'id', 'instance_id', 'user_id', 'started',
                            'finished', 'activity_code').all()

        for act in usr_acts:
            useful_data_chunk = dict(
                        id=act['id'],  # Activity ID
                        activity_code=act['activity_code'],  # What?
                        started=act['started'].strftime(
                            ACC_DATE_FORMAT),  # When did it started?
                        finished=act['finished'].strftime(
                            ACC_DATE_FORMAT),  # When did it finished?
                        user_id=act['user_id'],  # Who did that?
                        instance_id=act['instance_id'])  # Which machine

            instances = user.instance_set.filter
            (
                Q(id__exact=act['instance_id']),
                Q(owner_id__exact=act['user_id'])
            ).all()

            if len(instances) == 1:
                ins = instances[0]
                # Get all disks
                disks_ = ins.disks.all().values('size', 'id', 'datastore')

                useful_data_chunk['is_running'] = ins.is_running
                ins = instances.values('ram_size',
                                       'num_cores',
                                       'priority')[0]

                useful_data_chunk['ram'] = ins['ram_size']
                useful_data_chunk['cores'] = ins['num_cores']
                useful_data_chunk['core_prio'] = ins['priority']
                useful_data_chunk['disks'] = []

                for disk in disks_:
                    useful_data_chunk['disks'].append(disk)
            else:
                # Sharaed machine
                useful_data_chunk['ram'] = -1
                useful_data_chunk['cores'] = -1
                useful_data_chunk['core_prio'] = -1
                useful_data_chunk['disks'] = []

            temp_list.append(useful_data_chunk)
        return temp_list

    def write_data(self, filename=ACC_OUT_FILE):
        try:
            if self.is_collection_successfull:
                with open(filename, 'w') as file:
                    json.dump(
                        self.activities,
                        file,
                        indent=4,
                        separators=(',', ': ')
                    )
                return True
            else:
                print 'There is no data!'
                return False
        except Exception as e:
            print e
            return False

    def get_one_users_data(self, user=u'admin'):
        if self.is_collection_successfull:
            return self.activities[user]
        else:
            return None

    def get_data(self):
        if self.is_collection_successfull:
            return self.activities
        else:
            return None

    @property
    def is_successfull(self):
        return self.is_collection_successfull


# Makes report about the resource usage
class ReportMaker(models.Model):

    bills = JSONField(null=False, default={},
                      help_text='Every users bill.')
    
    start_date = DateTimeField(null=False,
                            help_text='Begining of the accounting.')
    
    end_date = DateTimeField(null=False, default=timezone.now,
                            help_text='End of the accounting'+
                            ' time intervall.')

    collector = ForeignKey(
        'ResourceCollector',
        limit_choices_to={'is_collection_successfull': True})

    @classmethod
    def create(cls, collector):
        reporter = cls(collector=collector)
        reporter.start_date = collector.start_date
        reporter.end_date = collector.end_date
        reporter.save()
        return reporter

    class Meta:
        app_label = 'accounting'
        db_table = 'acc_reportmaker'
        verbose_name = ('report_makers')
        verbose_name_plural = ('report_maker')
        ordering = ['-start_date']
        get_latest_by = 'start_date'
        
    def __str__(self):
        return u'Report_Maker'

    def make_report(self):
        if self.collector.is_collection_successfull:
            started = self.start_date.strftime(ACC_DATE_FORMAT)
            finished = self.end_date.strftime(ACC_DATE_FORMAT)
            
            for user in self.collector.activities.keys():
                file_name = user + '.txt'
                self.bills[user] = []
                
                user_bill = self.make_a_bill(user,
                        self.collector.activities[user])

                with open(file_name, 'w') as file:
                    json.dump(
                        self.bills,
                        file,
                        indent=4,
                        separators=[',', ': ']
                    )

                self.bills[user].append(user_bill)
            return True

        raise Exception('There is no data to work with!')

    def make_a_bill(self, user, activity_list):
        # the usage of the resources
        bill = dict()
        
        # every machine ID
        machines = self.get_machines(activity_list)
        
        # every activity for one machine
        activity_by_machines = self.get_acts(activity_list)
        
        for ins in machines:
            run_state = {'started': '',
                        'ended': '',
                        'renewed_times': 0} 
            bill[ins] = []
            # activity-k idő rendi sorrendben vannak
            for act in activity_by_machines[ins]:
                # tényleges költség számlázás
                if not act['ram'] == -1:  # másnak lesz számlázva a -1-es
                    if (
                        not act['activity_code'].rfind('deploy') == -1 or
                        not act['activity_code'].rfind('wake_up') == -1
                        ):
                        run_state['started'] = act['finished']
                    elif not act['activity_code'].rfind('renew') == -1:
                        run_state['renewed_times'] += 1
                    elif (
                        not act['activity_code'].rfind('sleep') == -1 or
                        not act['activity_code'].rfind('shut_off') == -1 or  #  off
                        not act['activity_code'].rfind('destroy') == -1
                        ):
                        run_state['ended'] = act['started']

                        if run_state['started'] == '': # T alatt szünt meg
                            earlier_ins_data = self.get_vm_earlier_data(
                                ins, user, self.start_date)
                            run_state['started'] = earlier_ins_data['start']
                            run_state['renewed_times'] += earlier_ins_data
                            ['renewed_cnt']
                        
                        temp_summ = self.get_runtime(run_state['started'], run_state['ended'])
                        temp_dict = {  # one running session
                                    'usaged_time': temp_summ,
                                    'used_ram': act['ram'],
                                    'used_cores': act['cores'],
                                    'cost': 'Not yet.',
                                    'cores_priority': act['core_prio'],
                                    'renewed': run_state['renewed_times'],
                                    'started': run_state['started'],
                                    'finished': run_state['ended']
                                }
                        
                        for disk in act['disks']:
                            temp_dict['disk_size'] = disk['size']
                        
                        bill[ins].append(temp_dict)
                        run_state.fromkeys(run_state, '') # reset
                else:
                    pass
        # a T alatt be nem fejezett futás nincs számlázva!
        return bill
    
    @classmethod
    def get_runtime(self, begin, end):
        dt = datetime.strptime(end, ACC_DATE_FORMAT) - datetime.strptime(begin, ACC_DATE_FORMAT)
        return str(dt)

    def get_machines(self, activity_list):
        if len(activity_list) == 0:
            return None

        machines = set()
        for act in activity_list:
            if not act['ram'] == -1:
                machines.add(act['instance_id'])
        return list(machines)

    def get_acts(self, activity_list):
        if len(activity_list) == 0:
            return None
        machines_acts = {activity_list[0]['instance_id']: []}
        for act in activity_list:
            if act['instance_id'] in machines_acts.keys():
                machines_acts[act['instance_id']].append(act)
                machines_acts[act['instance_id']] = sorted(
                    machines_acts[act['instance_id']],
                    key=itemgetter('id'))
            else:
                machines_acts[act['instance_id']] = []
                machines_acts[act['instance_id']].append(act)

        return machines_acts

    def get_vm_earlier_data(self, ins_id, user_name, date_to):
        print 'GET EARLIER DATA'
        user = User.objects.filter(username__exact=user_name).all()[0]

        date_to = datetime.strptime(date_to, ACC_DATE_FORMAT)
        date_from = date_to - timedelta(days=31,  # más
                                        hours=date_to.hour,
                                        minutes=date_to.minute,
                                        seconds=date_to.second)
        start_activity = {'start': '', 'renewed_cnt': 0}

        earlier_activities = user.instanceactivity_set.filter(
                            Q(instance_id__exact=ins_id),
                            Q(started__range=(date_from, date_to)),
                            Q(activity_code__exact='vm.Instance.deploy') |
                            Q(activity_code__exact='vm.Instance.wake_up') |
                            Q(activity_code__exact='vm.Instance.renew')
                            ).order_by('-started').all(
                            ).values('activity_code', 'finished')

        # idő szerint a legkésőbbi van elől (get prev act is van!)
        for act in earlier_activities:
            if 'vm.Instance.renew' in act['activity_code']:
                start_activity['renewed_cnt'] += 1

            if ('vm.Instance.deploy' in act['activity_code'] or
                    'vm.Instance.wake_up' in act['activity_code']):
                start_activity['start'] = act['finished'].strftime(ACC_DATE_FORMAT)
                break

        if start_activity['start'] == '':
            raise Exception('Hiba a feldolgozás során!')

        return start_activity

    def get_user_bill(self, this_user):
        if self.bills is None:
            return None
        
        if this_user is None:
            raise Exception('Given user is not given!')

        if this_user in self.bills.keys():
            return self.bills[this_user]
        else:
            raise Exception('User not found! ({0})'.format(this_user))

# TODO: Kitalálni hogy legyen...            
# class Bill(models.Model):
    
    # details = JSONField(default={},
                    # help_text='Details about the bill.')
    
    # owner_id = IntegerField(null=False, default=0,
                              # help_text='The payer.')
                              
    # total_used_ram = IntegerField(default=0)
    
    # total_used_cores = IntegerField(default=0)
    
    # total_used_disks = DecimalField(max_digits=8,
                                        # decimal_places=3)
    
    # total_used_time = DateTimeField(default=None)
    
    # total_cost = DecimalField(null=False, default = 0.0,
                    # max_digits=8, decimal_places=3)
    
    # maker = ForeignKey('ReportMaker')
    
    # @classmethod
    # def create(cls, report_maker):
        # if report_maker is None:
            # raise Exception('No maker given!')
            
        # raw_bills = report_maker.bills
        # self.users = raw_bills.keys() 
        # for user in self.users:
            
        
        # b = cls(maker=report_maker)
        
        # b.save()
        # return b
        
    # class Meta:
        # app_label = 'accounting'
        # db_table = 'acc_bill'
        # verbose_name = ('bills')
        # verbose_name_plural = ('bill')
        # ordering = ['owner']