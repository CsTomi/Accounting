#!/usr/env/bin python
# coding=utf-8
# vim: set fileencoding=utf-8


from accounting import ResourceCollector
from accounting import ReportMaker
import json

# Collector test, null parameters
def collector_test1():
    collector = ResourceCollector()  # dt=7
    print 'From: ', collector.start_date, '  To: ', collector.end_date
    collector.collect_data()
    data = collector.get_data()
    print data.keys()
    collector.write_data()
    
# collect one user's data
def collector_test2(user):
    collector = ResourceCollector()  # dt=7
    print 'From: ', collector.start_date, '  To: ', collector.end_date
    data=collector.collect_user_data( collector.start_date, collector.end_date, user)
    with open('test2.txt', 'w') as file:
         json.dump(data, file, indent=4, separators=(',', ': '))
         
# Collect data in the given interval
def collector_test3(start, end):
    collector = ResourceCollector(start=start, end=end)
    print 'From: ', collector.start_date, '  To: ', collector.end_date
    collector.collect_data()
    data = collector.get_data()
    print data.keys()
    collector.write_data()
    
def collector_test4(end, dt):
    collector = ResourceCollector(dt=dt, end=end)
    print 'From: ', collector.start_date, '  To: ', collector.end_date
    collector.collect_data()
    data = collector.get_data()
    print data.keys()
    collector.write_data()
    
def collector_test5(dt):
    collector = ResourceCollector(dt=dt)
    print 'From: ', collector.start_date, '  To: ', collector.end_date
    collector.collect_data()
    data = collector.get_data()
    print data.keys()
    collector.write_data()