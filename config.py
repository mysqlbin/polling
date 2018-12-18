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
start variables check
1.version

# InnoDB
1.innodb_flush_neighbors
2.innodb_flush_method
3.innodb_file_per_table
4.innodb_open_files
5.innodb_data_home_dir
6.innodb_io_capacity
7.innodb_lock_wait_timeout
8.innodb_thread_concurrency

# Redo
1.innodb_flush_log_at_trx_commit
2.innodb_log_file_size
4.innodb_log_files_in_group
5.innodb_log_buffer_size

# change buffer
1.innodb_change_buffer_max_size
2.innodb_change_buffering

# Other
1.sync_binlog
2.max_connections
3.query_cache_type
4.sort_buffer_size
5.read_buffer_size
6.max_allowed_packet
7.table_open_cache
8.thread_cache_size
9.key_buffer_size
10.字符集
11.time_zone
12.默认存储引擎
13.max_execution_time

----------------------------------------------------------------------------------------------------------------
'''

#1.mysql_version
sql_version = "select version();"
cursor.execute(sql_version)
data = cursor.fetchone()
mysql_version = data[0]
print "mysql_version: %-30s" % mysql_version

#InnoDB
#1.innodb_flush_neighbors
sql_innodb_flush_neighbors = "show global variables like 'innodb_flush_neighbors'"
cursor.execute(sql_innodb_flush_neighbors)
data = cursor.fetchone()
innodb_flush_neighbors = data[1]
print "innodb_flush_neighbors: %s" % innodb_flush_neighbors

#2.innodb_flush_method
sql_innodb_flush_method = "show global variables like 'innodb_flush_method'"
cursor.execute(sql_innodb_flush_method)
data = cursor.fetchone()
innodb_flush_method = data[1]
print "innodb_flush_method: %s" % innodb_flush_method

#3.innodb_file_per_table
sql_innodb_file_per_table = "show global variables like 'innodb_file_per_table'"
cursor.execute(sql_innodb_file_per_table)
data = cursor.fetchone()
innodb_file_per_table = data[1]
print "innodb_file_per_table: %s" % innodb_file_per_table

#4.innodb_open_files
sql_innodb_open_files = "show global variables like 'innodb_open_files'"
cursor.execute(sql_innodb_open_files)
data = cursor.fetchone()
innodb_open_files = data[1]
print "innodb_open_files: %s" % innodb_open_files

#5.innodb_data_home_dir
sql_innodb_data_home_dir = "show global variables like 'innodb_data_home_dir'"
cursor.execute(sql_innodb_data_home_dir)
data = cursor.fetchone()
innodb_data_home_dir = data[1]
print "innodb_data_home_dir: %s" % innodb_data_home_dir

#6.innodb_io_capacity
sql_innodb_io_capacity = "show global variables like 'innodb_io_capacity'"
cursor.execute(sql_innodb_io_capacity)
data = cursor.fetchone()
innodb_io_capacity = data[1]
print "innodb_io_capacity: %s" % innodb_io_capacity

#7.innodb_lock_wait_timeout
sql_innodb_lock_wait_timeout = "show global variables like 'innodb_lock_wait_timeout'"
cursor.execute(sql_innodb_lock_wait_timeout)
data = cursor.fetchone()
innodb_lock_wait_timeout = data[1]
print "innodb_lock_wait_timeout: %s" % innodb_lock_wait_timeout

#8.innodb_thread_concurrency
sql_innodb_thread_concurrency = "show global variables like 'innodb_thread_concurrency'"
cursor.execute(sql_innodb_thread_concurrency)
data = cursor.fetchone()
innodb_thread_concurrency = data[1]
print "innodb_thread_concurrency: %s" % innodb_thread_concurrency

#Redo
#1.innodb_flush_log_at_trx_commit
sql_innodb_flush_log_at_trx_commit = "show global variables like 'innodb_flush_log_at_trx_commit'"
cursor.execute(sql_innodb_flush_log_at_trx_commit)
data = cursor.fetchone()
innodb_flush_log_at_trx_commit = data[1]
print "innodb_flush_log_at_trx_commit: %s" % innodb_flush_log_at_trx_commit

#2.sql_innodb_log_file_size
sql_innodb_log_file_size = "show global variables like 'innodb_log_file_size'"
cursor.execute(sql_innodb_log_file_size)
data = cursor.fetchone()
innodb_log_file_size = int(data[1])/1024/1024
print "innodb_log_file_size: %f M" % innodb_log_file_size

#3.innodb_log_files_in_group
sql_innodb_flush_log_at_trx_commit = "show global variables like 'innodb_log_files_in_group'"
cursor.execute(sql_innodb_flush_log_at_trx_commit)
data = cursor.fetchone()
innodb_log_files_in_group = data[1]
print "innodb_log_files_in_group: %s" % innodb_log_files_in_group

#4.innodb_log_buffer_size
sql_innodb_log_buffer_size = "show global variables like 'innodb_log_buffer_size'"
cursor.execute(sql_innodb_log_buffer_size)
data = cursor.fetchone()
innodb_log_buffer_size = int(data[1])/1024/1024
print "innodb_log_buffer_size: %f M" % innodb_log_buffer_size

#Change buffer
#1.innodb_change_buffer_max_size
sql_innodb_change_buffer_max_size = "show global variables like 'innodb_change_buffer_max_size'"
cursor.execute(sql_innodb_change_buffer_max_size)
data = cursor.fetchone()
innodb_change_buffer_max_size = int(data[1])/1024/1024
print "innodb_change_buffer_max_size: %f M" % innodb_change_buffer_max_size

#2.innodb_change_buffering
sql_innodb_change_buffering = "show global variables like 'innodb_change_buffering'"
cursor.execute(sql_innodb_change_buffering)
data = cursor.fetchone()
innodb_change_buffering = data[1]
print "innodb_change_buffering: %s" % innodb_change_buffering

# Other
#1.sync_binlog
sql_sync_binlog = "show global variables like 'sync_binlog'"
cursor.execute(sql_sync_binlog)
data = cursor.fetchone()
sync_binlog = data[1]
print "sync_binlog: %s" % sync_binlog

#2.max_connections
sql_max_connections = "show global variables like 'max_connections'"
cursor.execute(sql_max_connections)
data = cursor.fetchone()
max_connections = data[1]
print "max_connections: %s" % max_connections

#3.query_cache_type
sql_query_cache_type = "show global variables like 'query_cache_type'"
cursor.execute(sql_query_cache_type)
data = cursor.fetchone()
query_cache_type = data[1]
print "query_cache_type: %s" % query_cache_type

#4.sort_buffer_size
sql_sort_buffer_size = "show global variables like 'sort_buffer_size'"
cursor.execute(sql_sort_buffer_size)
data = cursor.fetchone()
sort_buffer_size = float(data[1])/1024/1024
print "sort_buffer_size: %f M" % sort_buffer_size

#5.read_buffer_size
sql_read_buffer_size = "show global variables like 'read_buffer_size'"
cursor.execute(sql_read_buffer_size)
data = cursor.fetchone()
read_buffer_size = float(data[1])/1024/1024
print "read_buffer_size: %f M" % read_buffer_size

#6.max_allowed_packet
sql_max_allowed_packet = "show global variables like 'max_allowed_packet'"
cursor.execute(sql_max_allowed_packet)
data = cursor.fetchone()
max_allowed_packet = float(data[1])/1024/1024
print "max_allowed_packet: %f M" % max_allowed_packet

#7.table_open_cache
sql_table_open_cache = "show global variables like 'table_open_cache'"
cursor.execute(sql_table_open_cache)
data = cursor.fetchone()
table_open_cache = data[1]
print "table_open_cache: %s" % table_open_cache

#8.thread_cache_size
sql_thread_cache_size = "show global variables like 'thread_cache_size'"
cursor.execute(sql_thread_cache_size)
data = cursor.fetchone()
thread_cache_size = data[1]
print "thread_cache_size: %s" % thread_cache_size


#9.key_buffer_size
sql_key_buffer_size = "show global variables like 'key_buffer_size'"
cursor.execute(sql_key_buffer_size)
data = cursor.fetchone()
key_buffer_size = float(data[1])/1024/1024
print "key_buffer_size: %f M" % key_buffer_size

#10.charset
sql_character_set_server = "show global variables like 'character_set_server'"
cursor.execute(sql_character_set_server)
data = cursor.fetchone()
character_set_server = data[1]
print "character_set_server: %s" % character_set_server

#11.time_zone
sql_time_zone = "show global variables like 'time_zone'"
cursor.execute(sql_time_zone)
data = cursor.fetchone()
time_zone = data[1]
print "time_zone: %s" % time_zone

#12.default_storage_engine
sql_default_storage_engine = "show global variables like 'default_storage_engine'"
cursor.execute(sql_default_storage_engine)
data = cursor.fetchone()
default_storage_engine = data[1]
print "default_storage_engine: %s" % default_storage_engine

#13.max_execution_time
sql_max_execution_time = "show global variables like 'max_execution_time'"
cursor.execute(sql_max_execution_time)
data = cursor.fetchone()
max_execution_time = data[1]
print "max_execution_time: %s" % max_execution_time