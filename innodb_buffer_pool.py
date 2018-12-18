#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import MySQLdb
import time,datetime
import re

conn = MySQLdb.connect(host='192.168.0.54', port=3306, user='root', passwd='123456abc', db='niuniu_db', charset='utf8')
cursor = conn.cursor()

print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "++                                          MySQL Check report                                                ++"
print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

print "start time: %s" % datetime.datetime.now()
#table_check


print '''
----------------------------------------------------------------------------------------------------------------
start innodb_buffer_pool check
1.innodb_buffer_pool_size                   #缓冲池大小
2.innodb_lru_scan_depth                     #控制LRU列表中可用页的数量，默认值为1024
3.innodb_buffer_pool_instances              #缓冲池实例数
4.innodb_max_dirty_pages_pct                #达到最大脏页占比，强制进行 checkpoint, 刷新一部分的脏页到磁盘
5.innodb_buffer_pool_pages_dirty            #脏页数据的大小
6.innodb_buffer_pool_pages_total            #页总数
7.innodb_buffer_pool_read_requests          #从缓冲池读取页的次数
8.innodb_buffer_pool_read_ahead             #预读的次数
9.innodb_buffer_pool_reads                  #从磁盘读取页的次数
10.计算脏页占比  innodb_buffer_pool_pages_dirty/innodb_buffer_pool_pages_total
11.计算InnoDB buffer pool 命中率 innodb_buffer_pool_read_requests/(innodb_buffer_pool_read_requests + innodb_buffer_pool_read_ahead + innodb_buffer_pool_reads)

----------------------------------------------------------------------------------------------------------------
'''

#1.innodb_buffer_pool_size
sql_innodb_buffer_pool_size = "show global variables like 'innodb_buffer_pool_size'"
cursor.execute(sql_innodb_buffer_pool_size)
data = cursor.fetchone()
innodb_buffer_pool_size = int(data[1])/1024/1024
print "innodb_buffer_pool_size: %f M" % innodb_buffer_pool_size

#2.innodb_lru_scan_depth
sql_innodb_lru_scan_depth = "show global variables like 'innodb_lru_scan_depth'"
cursor.execute(sql_innodb_lru_scan_depth)
data = cursor.fetchone()
innodb_lru_scan_depth = data[1]
print "innodb_lru_scan_depth: %s" % innodb_lru_scan_depth

#3.innodb_buffer_pool_instances
sql_innodb_buffer_pool_instances = "show global variables like 'innodb_buffer_pool_instances'"
cursor.execute(sql_innodb_buffer_pool_instances)
data = cursor.fetchone()
innodb_buffer_pool_instances = data[1]
print "innodb_buffer_pool_instances: %s" % innodb_buffer_pool_instances

#4.innodb_max_dirty_pages_pct
sql_innodb_max_dirty_pages_pct = "show global variables like 'innodb_max_dirty_pages_pct'"
cursor.execute(sql_innodb_max_dirty_pages_pct)
data = cursor.fetchone()
innodb_max_dirty_pages_pct = data[1]
print "innodb_max_dirty_pages_pct: %s" % innodb_max_dirty_pages_pct


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

#7.innodb_buffer_pool_read_requests
sql_innodb_buffer_pool_read_requests = "show global status like 'innodb_buffer_pool_read_requests'"
cursor.execute(sql_innodb_buffer_pool_read_requests)
data = cursor.fetchone()
innodb_buffer_pool_read_requests = data[1]
print "innodb_buffer_pool_read_requests: %s" % innodb_buffer_pool_read_requests


#8.innodb_buffer_pool_read_ahead
sql_innodb_buffer_pool_read_ahead = "show global status like 'innodb_buffer_pool_read_ahead'"
cursor.execute(sql_innodb_buffer_pool_read_ahead)
data = cursor.fetchone()
innodb_buffer_pool_read_ahead = data[1]
print "innodb_buffer_pool_read_ahead: %s" % innodb_buffer_pool_read_ahead


#9.innodb_buffer_pool_reads
sql_innodb_buffer_pool_reads = "show global status like 'innodb_buffer_pool_reads'"
cursor.execute(sql_innodb_buffer_pool_reads)
data = cursor.fetchone()
innodb_buffer_pool_reads = data[1]
print "innodb_buffer_pool_reads: %s" % innodb_buffer_pool_reads

#计算脏页占比  innodb_buffer_pool_pages_dirty/innodb_buffer_pool_pages_total
dirty_page = round(float(innodb_buffer_pool_pages_dirty)/int(innodb_buffer_pool_pages_total),4)
dirty_page_percent = "%.2f%%" % (dirty_page*100)
print "脏页占比: %s" % dirty_page_percent

#计算InnoDB buffer pool 命中率 innodb_buffer_pool_read_requests/(innodb_buffer_pool_read_requests + innodb_buffer_pool_read_ahead + innodb_buffer_pool_reads)
rate = round(float(innodb_buffer_pool_read_requests)/(int(innodb_buffer_pool_read_requests) + int(innodb_buffer_pool_read_ahead) + int(innodb_buffer_pool_reads)), 4)
rate_percent = "%.2f%%" % (rate*100)
print "InnoDB buffer pool 命中率: %s" %  rate_percent
