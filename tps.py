#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import MySQLdb
import time,datetime
import re

conn = MySQLdb.connect(host='192.168..', port=3306, user='root', passwd='', db='', charset='utf8')
cursor = conn.cursor()



def sql_value(status):
    sql_global_status = "show global status like \'%s\'" % status
    cursor.execute(sql_global_status)
    data = cursor.fetchone()
    return data[1]

for i in range(10):

    print "start time: %s" % datetime.datetime.now()

    print '''
    ----------------------------------------------------------------------------------------------------------------
    '''
    print("loop:", i)

    sql_cc_start = sql_value('Com_commit')
    sql_cr_start = sql_value('Com_rollback')
    sql_uptime_start = sql_value('Uptime')

    time.sleep(60)

    sql_cc_end = sql_value('Com_commit')
    sql_cr_end = sql_value('Com_rollback')
    sql_uptime_end = sql_value('Uptime')

    #rate = round(float(innodb_buffer_pool_read_requests)/(int(innodb_buffer_pool_read_requests) + int(innodb_buffer_pool_read_ahead) + int(innodb_buffer_pool_reads)), 4)
    #(sql_untime_start - sql_uptime_end)
    #(sql_cc_end + sql_cr_end) - (sql_cc_start + sql_cr_start)

    TPS = (int(int(sql_cc_end) + int(sql_cr_end)) - int(int(sql_cc_start) + int(sql_cr_start))) / int(int(sql_uptime_end) - int(sql_uptime_start))

    print TPS

    print "end time: %s" % datetime.datetime.now()

    print '''
        ----------------------------------------------------------------------------------------------------------------
        '''

    #TPS = ((Cc2+Cr2)-(Cc1+Cr1)) / (T2-T1);







