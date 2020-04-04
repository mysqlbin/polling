#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import MySQLdb
import time,datetime
import re
import sys

'''
sys.argv[1]   #version
sys.argv[2]   #host
sys.argv[3]   #b_name
'''

conn = MySQLdb.connect(host=sys.argv[2], port=3306, user='polling_user', passwd='', db=sys.argv[3], charset='utf8')
cursor = conn.cursor()


print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "++                                          MySQL Check report                                                ++"
print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

print "start time: %s" % datetime.datetime.now()

print '''
----------------------------------------------------------------------------------------------------------------
'''
print "\033[1;33;46m start table check\033[0m"

print '''
----------------------------------------------------------------------------------------------------------------

1.超过1G大表
2.数据量排名前20的表
3.碎片超过0.5G的表
4.自增ID占比超过50%;
----------------------------------------------------------------------------------------------------------------
'''
#1.get tables more than 10G
cursor.execute("select table_schema,table_name,concat(round((data_length+index_length)/1024/1024,2),'M') FROM \
information_schema.tables where (DATA_LENGTH+INDEX_LENGTH) > 1*1024*1024*1024  and table_schema not in \
('information_schema','mysql','performance_schema','sys')")
table_size = cursor.fetchall()

print "\033[1;33;44m 1: result of table is more than 1G\033[0m"
if table_size:
    for table in table_size:
        table_schema = table[0]
        table_name = table[1]
        size = table[2]
        print " table_schema: %-20s  table_name : %-20s size: %10s " % \
              (table_schema, table_name, size)
else:
    print "no table is more than 1G"

#2.get the top 20 tables
cursor.execute("SELECT table_schema,table_name,(data_length/1024/1024) AS data_mb,(index_length/1024/1024) AS index_mb,((data_length + index_length)/1024/1024) AS all_mb,table_rows FROM  \
information_schema.tables  where table_schema not in \
('information_schema','mysql','performance_schema','sys') order by all_mb desc limit 20")
table_size_20 = cursor.fetchall()

print "\033[1;33;44m 2: result of the top 20 tables\033[0m"
if table_size_20:
    for table in table_size_20:
        table_schema = table[0]
        table_name = table[1]
        data_size = table[2]
        index_size = table[3]
        all_size = table[4]
        table_rows = table[5]
        print " table_schema: %-10s  table_name : %-30s all_size: %-15s data_size: %-15s index_size: %-15s rows: %-5s" % \
              (table_schema, table_name, all_size, data_size, index_size, table_rows)
else:
    print "no tabls the top 20"

#3.get tables which have big fragment
cursor.execute("select table_schema,table_name,DATA_FREE from \
information_schema.TABLES where table_schema not in ('information_schema','mysql','performance_schema','sys') \
and data_free > 0.5*1024*1024*1024 order by DATA_FREE desc;")
table_fragment = cursor.fetchall()

print "\033[1;33;44m 3: result of table has big fragment\033[0m"
if table_fragment:
    for table in table_fragment:
        table_schema = table[0]
        table_name = table[1]
        data_free = table[2]
        print " table_schema: %-20s  table_name : %-20s fragment: %10s " % \
              (table_schema, table_name, data_free) 
else:
    print "no table has big fragment"


#4.auto increment ratio

if sys.argv[1] == '5.7':
    cursor.execute("select table_schema,table_name,max_value,auto_increment,auto_increment_ratio from sys.schema_auto_increment_columns  \
    where auto_increment_ratio > '0.5000' and table_schema not in \
    ('information_schema','mysql','performance_schema','sys') order by auto_increment_ratio desc;")
    auto_increment = cursor.fetchall()

    print "\033[1;33;44m 4: result of auto increment ratio\033[0m"
    if auto_increment:
        for table in auto_increment:
            table_schema = table[0]
            table_name = table[1]
            max_value = table[2]
            auto_increment = table[3]
            auto_increment_ratio = table[4]
            print " table_schema: %-20s  table_name : %-30s all_size: %-15s data_size: %-15s index_size: %-15s " % \
                  (table_schema, table_name, max_value, auto_increment, auto_increment_ratio)
    else:
        print "no table auto increment ratio has more than 50%"


print '''
----------------------------------------------------------------------------------------------------------------
'''
print "\033[1;33;46m start transactions/locks check\033[0m"

print '''
----------------------------------------------------------------------------------------------------------------
1.长时间未提交的事务

----------------------------------------------------------------------------------------------------------------
'''
#long uncommitted transactions
cursor.execute("select b.host, b.user, b.db, b.time, b.COMMAND, a.trx_id, a. trx_state   \
from information_schema.innodb_trx a left join information_schema.PROCESSLIST b on a.trx_mysql_thread_id = b.id;")
long_transactions = cursor.fetchall()
print "\033[1;33;44m 1: result of long uncommitted transactions\033[0m"
if long_transactions:
    for trx in long_transactions:
        host = trx[0]
        user = trx[1]
        db_name = trx[2]
        time = trx[3]
        command = trx[4]
        trx_id = trx[5]
        trx_state = trx[6]
        print " host: %-20s  user: %-20s db_name: %-20s time: %-20s command: %-20s trx_id: %-20s trx_state: %-20s" % \
              (host, user, db_name, time, command, trx_id, trx_state)
else:
    print "no long uncommitted transactions"

print '''
----------------------------------------------------------------------------------------------------------------
'''
print "\033[1;33;46m start variables check\033[0m"
#config
print '''
----------------------------------------------------------------------------------------------------------------
1.version
2.Innodb_log_waits  #因 log buffer不足导致等待的次数
3.max_connections   #当前数据库的最大连接数
4.Max_used_connections  #当前已使用的数据库连接数
5.innodb_buffer_pool_pages_dirty            #脏页数据的大小
6.innodb_buffer_pool_pages_total            #缓冲池全部页的个数（page总数）
7.计算脏页占比  innodb_buffer_pool_pages_dirty/innodb_buffer_pool_pages_total
8.innodb_buffer_pool_read_requests          #从缓冲池读取页的次数
9.innodb_buffer_pool_read_ahead             #预读的次数
10.innodb_buffer_pool_reads                  #从磁盘读取页的次数
11.计算InnoDB buffer pool 命中率 innodb_buffer_pool_read_requests/(innodb_buffer_pool_read_requests + innodb_buffer_pool_read_ahead + innodb_buffer_pool_reads)
12.Innodb_buffer_pool_wait_free             #innodb buffer pool不够用了等待把热点数据或脏页的buffer pool释放次数，该参数大于0说明  InnoDB buffer pool 不够用了
13. Innodb_buffer_pool_pages_free           #空闲的page数量
14.Threads_running                          #表示当前正在运行的活跃线程数
15.Innodb_row_lock_current_waits            #表示当前发生行锁等待的次数
16.tmp_tables　tmp_disk_tables　　　　　　　#临时表、磁盘临时表　　　　
----------------------------------------------------------------------------------------------------------------
'''


#1.mysql_version
sql_version = "select version();"
cursor.execute(sql_version)
data = cursor.fetchone()
mysql_version = data[0]
print "mysql_version: %-30s" % mysql_version

#2.Innodb_log_waits
sql_Innodb_log_waits = "show global status like 'Innodb_log_waits'"
cursor.execute(sql_Innodb_log_waits)
data = cursor.fetchone()
Innodb_log_waits = data[1]
print '因 log buffer不足导致等待的次数(Innodb_log_waits): %s' %  int(Innodb_log_waits) + ' 次'

#3.max_connections
sql_max_connections = "show global variables like 'max_connections'"
cursor.execute(sql_max_connections)
data = cursor.fetchone()
max_connections = data[1]
print "max_connections: %s" % max_connections

#4.Max_used_connections
sql_Max_used_connections = "show global status like 'Max_used_connections'"
cursor.execute(sql_Max_used_connections)
data = cursor.fetchone()
Max_used_connections = data[1]
print "Max_used_connections: %s" % Max_used_connections



#5.innodb_buffer_pool_pages_dirty
sql_innodb_buffer_pool_pages_dirty = "show global status like 'innodb_buffer_pool_pages_dirty'"
cursor.execute(sql_innodb_buffer_pool_pages_dirty)
data = cursor.fetchone()
innodb_buffer_pool_pages_dirty = data[1]
print "innodb_buffer_pool_pages_dirty: %s" % innodb_buffer_pool_pages_dirty

#6.innodb_buffer_pool_pages_total
sql_innodb_buffer_pool_pages_total = "show global status like 'innodb_buffer_pool_pages_total'"
cursor.execute(sql_innodb_buffer_pool_pages_total)
data = cursor.fetchone()
innodb_buffer_pool_pages_total = data[1]
print "innodb_buffer_pool_pages_total: %s" % innodb_buffer_pool_pages_total


#7.计算脏页占比  innodb_buffer_pool_pages_dirty/innodb_buffer_pool_pages_total
dirty_page = round(float(innodb_buffer_pool_pages_dirty)/int(innodb_buffer_pool_pages_total),4)
dirty_page_percent = "%.2f%%" % (dirty_page*100)
print "脏页占比: %s" % dirty_page_percent


#8.innodb_buffer_pool_read_requests
sql_innodb_buffer_pool_read_requests = "show global status like 'innodb_buffer_pool_read_requests'"
cursor.execute(sql_innodb_buffer_pool_read_requests)
data = cursor.fetchone()
innodb_buffer_pool_read_requests = data[1]
print "innodb_buffer_pool_read_requests: %s" % innodb_buffer_pool_read_requests


#9.innodb_buffer_pool_read_ahead
sql_innodb_buffer_pool_read_ahead = "show global status like 'innodb_buffer_pool_read_ahead'"
cursor.execute(sql_innodb_buffer_pool_read_ahead)
data = cursor.fetchone()
innodb_buffer_pool_read_ahead = data[1]
print "innodb_buffer_pool_read_ahead: %s" % innodb_buffer_pool_read_ahead

#10.innodb_buffer_pool_reads
sql_innodb_buffer_pool_reads = "show global status like 'innodb_buffer_pool_reads'"
cursor.execute(sql_innodb_buffer_pool_reads)
data = cursor.fetchone()
innodb_buffer_pool_reads = data[1]
print "innodb_buffer_pool_reads: %s" % innodb_buffer_pool_reads


#11.计算InnoDB buffer pool 命中率 innodb_buffer_pool_read_requests/(innodb_buffer_pool_read_requests + innodb_buffer_pool_read_ahead + innodb_buffer_pool_reads)
rate = round(float(innodb_buffer_pool_read_requests)/(int(innodb_buffer_pool_read_requests) + int(innodb_buffer_pool_read_ahead) + int(innodb_buffer_pool_reads)), 4)
rate_percent = "%.2f%%" % (rate*100)
print "InnoDB buffer pool 命中率: %s" %  rate_percent


#12.Innodb_buffer_pool_wait_free
sql_innodb_buffer_pool_wait_free = "show global status like 'Innodb_buffer_pool_wait_free'"
cursor.execute(sql_innodb_buffer_pool_wait_free)
data = cursor.fetchone()
innodb_buffer_pool_wait_free = data[1]
print "Innodb_buffer_pool_wait_free: %s" % innodb_buffer_pool_wait_free


#13.Innodb_buffer_pool_pages_free
sql_Innodb_buffer_pool_pages_free = "show global status like 'Innodb_buffer_pool_pages_free'"
cursor.execute(sql_Innodb_buffer_pool_pages_free)
data = cursor.fetchone()
innodb_buffer_pool_pages_free = data[1]
print 'Innodb buffer pool空闲Page的数量(Innodb_buffer_pool_pages_free): %s' %  int(innodb_buffer_pool_pages_free) + '　个Page'


#14.Threads_running
sql_Threads_running = "show global status like 'Threads_running'"
cursor.execute(sql_Threads_running)
data = cursor.fetchone()
Threads_running = data[1]
print "Threads_running: %s" % Threads_running

#15.Innodb_row_lock_current_waits
sql_Innodb_row_lock_current_waits = "show global status like 'Innodb_row_lock_current_waits'"
cursor.execute(sql_Innodb_row_lock_current_waits)
data = cursor.fetchone()
Innodb_row_lock_current_waits = data[1]
print "Innodb_row_lock_current_waits: %s" % Innodb_row_lock_current_waits

if Innodb_row_lock_current_waits > 0:
    if sys.argv[1] >= '5.7':
        cursor.execute("SELECT locked_index,locked_type,waiting_query,waiting_lock_mode,blocking_lock_mode FROM sys.innodb_lock_waits;")
        innodb_lock_waits = cursor.fetchall()
        print "\033[1;33;44m 1: result of innodb row lock current waits\033[0m"
        if innodb_lock_waits:
            for trx in innodb_lock_waits:
                locked_index = trx[0]
                locked_type = trx[1]
                waiting_query = trx[2]
                waiting_lock_mode = trx[3]
                blocking_lock_mode = trx[4]
                print " locked_index: %-20s  locked_type: %-20s waiting_query: %-20s waiting_lock_mode: %-20s blocking_lock_mode: %-20s" % \
                      (locked_index, locked_type, waiting_query, waiting_lock_mode, blocking_lock_mode)
        else:
            print "no innodb row lock current waits"
    else:

        cursor.execute(
            "select requesting_trx_id,requested_lock_id,blocking_trx_id,blocking_lock_id from information_schema.INNODB_LOCK_WAITS;")
        innodb_lock_waits = cursor.fetchall()
        print "\033[1;33;44m 1: result of long uncommitted transactions\033[0m"
        if innodb_lock_waits:
            for trx in innodb_lock_waits:
                requesting_trx_id = trx[0]
                requested_lock_id = trx[1]
                blocking_trx_id = trx[2]
                blocking_lock_id = trx[3]
                print " blocking_lock_id: %-20s  requested_lock_id: %-20s blocking_trx_id: %-20s blocking_lock_id: %-20s" % \
                      (blocking_lock_id, requested_lock_id, blocking_trx_id, blocking_lock_id)
        else:
            print "no innodb row lock current waits"

#16.tmp_tables, tmp_disk_tables
if sys.argv[1] >= '5.7':
    cursor.execute(
        "select db, query, tmp_tables, tmp_disk_tables, tmp_tables+tmp_disk_tables as tmp_all from sys.statement_analysis where tmp_tables>0 or tmp_disk_tables >0 order by tmp_all desc limit 20;")
    tmp_tables = cursor.fetchall()
    print "\033[1;33;44m 1: result of tmp_tables list \033[0m"
    if tmp_tables:
        for trx in tmp_tables:
            db_name = trx[0]
            query_sql = trx[1]
            tmp_tables = trx[2]
            tmp_disk_tables = trx[3]
            tmp_all = trx[4]
            print " db_name: %-20s  query_sql: %-20s tmp_tables: %-20s tmp_disk_tables: %-20s tmp_all: %-20s" % \
                  (db_name, query_sql, tmp_tables, tmp_disk_tables, tmp_all)
    else:
        print "no tmp_tables data"


print '''
----------------------------------------------------------------------------------------------------------------
'''

print "end time: %s" % datetime.datetime.now()