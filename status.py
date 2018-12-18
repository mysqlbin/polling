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
start status check
      1).当前并发连接数:
		Threads_connected  表示当前所有已经连接的线程数
		Threads_created    表示当前所有已经创建的线程数
		Threads_running    表示当前正在运行的线程数

	  2).行锁等待:
		Innodb_row_lock_current_waits  表示当前发生行锁等待的次数
		Innodb_row_lock_time        表示当前发生行锁等待的总时间（以毫秒为单位）
		Innodb_row_lock_time_avg    表示当前发生行锁等待的平均时间（以毫秒为单位）
		Innodb_row_lock_time_max    表示当前发生行锁等待的最大时间（以毫秒为单位）
		Innodb_row_lock_waits       表示发生行锁等待的总次数

	  3). opend_files
	  4). opend_tables
	  5). Max_used_connections

----------------------------------------------------------------------------------------------------------------
'''

#1.opened files
sql_Opened_files = "show global status like 'Opened_files'"
cursor.execute(sql_Opened_files)
data = cursor.fetchone()
Opened_files = data[1]
print "Opened_files: %s" % Opened_files

#2.Opened_table_definitions files
sql_Opened_table_definitions = "show global status like 'Opened_table_definitions'"
cursor.execute(sql_Opened_table_definitions)
data = cursor.fetchone()
Opened_table_definitions = data[1]
print "Opened_table_definitions: %s" % Opened_table_definitions

#3.Opened_tables
sql_Opened_tables = "show global status like 'Opened_tables'"
cursor.execute(sql_Opened_tables)
data = cursor.fetchone()
Opened_tables = data[1]
print "Opened_tables: %s" % Opened_tables

#4.Max_used_connections
sql_Max_used_connections = "show global status like 'Max_used_connections'"
cursor.execute(sql_Max_used_connections)
data = cursor.fetchone()
Max_used_connections = data[1]
print "Max_used_connections: %s" % Max_used_connections
