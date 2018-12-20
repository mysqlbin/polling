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

print '''
----------------------------------------------------------------------------------------------------------------
'''
print "\033[1;33;46m start table check\033[0m"

print '''
----------------------------------------------------------------------------------------------------------------

1.size
2.top 20 tables
3.much indexes
4.fragment
5.rows
6.charset
7.big column
8.long column
9.auto increment ratio
----------------------------------------------------------------------------------------------------------------
'''
#1.get tables more than 10G
cursor.execute("select table_schema,table_name,concat(round((data_length+index_length)/1024/1024,2),'M') FROM \
information_schema.tables where (DATA_LENGTH+INDEX_LENGTH) > 10*1024*1024*1024  and table_schema not in \
('information_schema','mysql','performance_schema','sys')")
table_size = cursor.fetchall()

print "\033[1;33;44m 1: result of table is more than 10G\033[0m"
if table_size:
    for table in table_size:
        table_schema = table[0]
        table_name = table[1]
        size = table[2]
        print " table_schema: %-20s  table_name : %-20s size: %10s " % \
              (table_schema, table_name, size)
else:
    print "no table is more than 10G"

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
        print " table_schema: %-20s  table_name : %-30s all_size: %-15s data_size: %-15s index_size: %-15s rows: %-5s" % \
              (table_schema, table_name, all_size, data_size, index_size, table_rows)
else:
    print "no tabls the top 20"

#3.get tables which have more than 6 indexes
cursor.execute("select t1.name,t2.num from information_schema.innodb_sys_tables t1, (select table_id,count(*) as num from \
information_schema.innodb_sys_indexes group by table_id having count(*) >=6) t2 where t1.table_id =t2.table_id")
table_index = cursor.fetchall()

print "\033[1;33;44m 3: result of table more than 6 indexes\033[0m"
if table_index:
    for table in table_index:
        table_name = table[0]
        index_num = table[1]
        print " table_name: %-50s  index_num: %10d " % \
              (table_name, index_num)
else:
    print "no table has more than 6 indexes"


#4.get tables which have big fragment
cursor.execute("select table_schema,table_name,DATA_FREE from \
information_schema.TABLES where table_schema not in ('information_schema','mysql','performance_schema','sys') \
and data_free > 1*1024*1024*1024 order by DATA_FREE desc;")
table_fragment = cursor.fetchall()

print "\033[1;33;44m 4: result of table has big fragment\033[0m"
if table_fragment:
    for table in table_fragment:
        table_schema = table[0]
        table_name = table[1]
        data_free = table[2]
        print " table_schema: %-20s  table_name : %-20s fragment: %10s " % \
              (table_schema, table_name, data_free)
else:
    print "no table has big fragment"

#5.get tables which have 20000000 rows
cursor.execute("select table_schema,table_name,table_rows from \
information_schema.TABLES where table_schema not in ('information_schema','mysql','performance_schema','sys') \
and table_rows > 20000000 order by table_rows desc;")
table_fragment = cursor.fetchall()

print "\033[1;33;44m 5: result of table has more than 20000000 rows\033[0m"
if table_fragment:
    for table in table_fragment:
        table_schema = table[0]
        table_name = table[1]
        table_rows = table[2]
        print " table_schema: %-20s  table_name : %-20s table_rows: %10d " % \
              (table_schema, table_name, table_rows)
else:
    print "no table has has more than 20000000 rows"

#6.get table charset not default
cursor.execute("show variables like 'character_set_server';")
default_charset = str(cursor.fetchone()[1])
default_charset = default_charset+"_general_ci"
sql = "select table_schema,table_name,table_collation from information_schema.tables where table_schema not \
in ('information_schema','mysql','performance_schema','sys') and table_collation !='"+default_charset+"';"
cursor.execute(sql)
table_charset = cursor.fetchall()

print "\033[1;33;44m 6: result of table is not in default charset\033[0m"
if table_charset:
    for table in table_charset:
        table_schema = table[0]
        table_name = table[1]
        charset = table[2]
        print " table_schema: %-20s  table_name : %-20s charset: %10s " % \
              (table_schema, table_name, charset)
else:
    print "no table is not in default charset"

#7.get tables which have big columns
cursor.execute("select table_schema,table_name,column_name,data_type from information_schema.columns where data_type in \
('blob','clob','text','medium text','long text') and table_schema not in \
('information_schema','performance_schema','mysql','sys')")
table_big_cols = cursor.fetchall()

print "\033[1;33;44m 7: result of table has big columns\033[0m"
if table_big_cols:
    for table in table_big_cols:
        table_schema = table[0]
        table_name = table[1]
        column_name = table[2]
        data_type = table[3]
        print " table_schema: %-20s  table_name : %-20s column_name: %-20s data_type: %-20s" % \
              (table_schema, table_name, column_name, data_type)
else:
    print "no table has has big columns"

#8.get tables which have long varchar columns
cursor.execute("select table_schema,table_name,column_name,data_type,CHARACTER_MAXIMUM_LENGTH from information_schema.columns \
where DATA_TYPE='varchar' and CHARACTER_MAXIMUM_LENGTH > 500 and table_schema not in \
('information_schema','performance_schema','mysql','sys');")
table_long_cols = cursor.fetchall()

print "\033[1;33;44m 8: result of table has long columns\033[0m"
if table_long_cols:
    for table in table_long_cols:
        table_schema = table[0]
        table_name = table[1]
        column_name = table[2]
        data_type = table[3]
        CHARACTER_MAXIMUM_LENGTH = table[4]
        print " table_schema: %-20s  table_name : %-20s column_name: %-20s data_type: %-20s length: %-5s" % \
              (table_schema, table_name, column_name, data_type, CHARACTER_MAXIMUM_LENGTH)
else:
    print "no table has has big columns"

#9.auto increment ratio
cursor.execute("select table_schema,table_name,max_value,auto_increment,auto_increment_ratio from sys.schema_auto_increment_columns  \
where auto_increment_ratio > '0.0001' and table_schema not in \
('information_schema','mysql','performance_schema','sys') order by auto_increment_ratio desc")
auto_increment = cursor.fetchall()

print "\033[1;33;44m 9: result of auto increment ratio\033[0m"
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
print "\033[1;33;46m start index check\033[0m"

print '''
----------------------------------------------------------------------------------------------------------------
1.get tables which have not indexes
2.redundant indexes
3.to much columns indexes
4.unused indexes
5.sub_part indexes
----------------------------------------------------------------------------------------------------------------
'''

#get tables which have not indexes
cursor.execute("SELECT t.table_schema,t.table_name FROM information_schema.tables AS t LEFT JOIN \
(SELECT DISTINCT table_schema, table_name FROM information_schema.`KEY_COLUMN_USAGE` ) AS kt ON \
kt.table_schema=t.table_schema AND kt.table_name = t.table_name WHERE t.table_schema NOT IN \
('mysql', 'information_schema', 'performance_schema', 'sys') AND kt.table_name IS NULL;")
table_not_indexes = cursor.fetchall()

print "\033[1;33;44m 1: result of table has not indexes\033[0m"
if table_not_indexes:
    for table in table_not_indexes:
        table_schema = table[0]
        table_name = table[1]
        print " table_schema: %-20s  table_name : %-20s " % \
              (table_schema, table_name)
else:
    print "all tables have indexes"

#redundant indexes
cursor.execute("select table_schema,table_name,redundant_index_name,redundant_index_columns \
from sys.schema_redundant_indexes;")
redundant_indexes = cursor.fetchall()

print "\033[1;33;44m 2: result of redundant indexes\033[0m"
if redundant_indexes:
    for index in redundant_indexes:
        table_schema = index[0]
        table_name = index[1]
        index_name = index[2]
        column_name = index[3]
        print " table_schema: %-20s  table_name: %-20s index_name: %-20s column_name:%-20s" % \
              (table_schema, table_name, index_name, column_name)
else:
    print "no redundant indexes"


#to much columns indexes
cursor.execute("select s.table_schema,s.table_name,s.index_name,s.column_name from information_schema.STATISTICS s,\
(select table_name,index_name,count(*) from information_schema.STATISTICS where table_schema not in \
('information_schema','performance_schema','mysql','sys') group by table_name,index_name having count(*)>5)t where \
s.table_name=t.table_name and s.index_name=t.index_name;")
to_much_columns_indexes = cursor.fetchall()

print "\033[1;33;44m 3: result of to much columns indexes\033[0m"
if to_much_columns_indexes:
    for index in to_much_columns_indexes:
        table_schema = index[0]
        table_name = index[1]
        index_name = index[2]
        column_name = index[3]
        print " table_schema: %-20s  table_name: %-20s index_name: %-20s column_name:%-20s" % \
              (table_schema, table_name, index_name, column_name)
else:
    print "all index have column under 5"


#unused indexes
cursor.execute("select * from sys.schema_unused_indexes;")
unused_indexes = cursor.fetchall()
print "\033[1;33;44m 4: result of redundant indexes\033[0m"
if unused_indexes:
    for index in unused_indexes:
        table_schema = index[0]
        table_name = index[1]
        index_name = index[2]
        print " table_schema: %-20s  table_name: %-45s index_name: %-20s" % \
              (table_schema, table_name, index_name)
else:
    print "no unused indexes"

#sub_part indexes
cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME, INDEX_NAME, COLUMN_NAME, CARDINALITY, SUB_PART  \
FROM INFORMATION_SCHEMA.STATISTICS WHERE SUB_PART > 10 ORDER BY SUB_PART DESC;")
sub_part_indexes = cursor.fetchall()
print "\033[1;33;44m 5: result of sub_part indexes\033[0m"
if sub_part_indexes:
    for index in sub_part_indexes:
        table_schema = index[0]
        table_name = index[1]
        index_name = index[2]
        column_name = index[3]
        cardinality = index[4]
        sub_part = index[5]
        print " table_schema: %-20s  table_name: %-45s index_name: %-20s column_name: %-20s cardinality: %-20s sub_part: %-20s" % \
              (table_schema, table_name, index_name, column_name, cardinality, sub_part)
else:
    print "no sub_part indexes"

time.sleep(1)


print '''
----------------------------------------------------------------------------------------------------------------
'''
print "\033[1;33;46m start transactions/locks check\033[0m"

print '''
----------------------------------------------------------------------------------------------------------------
1.long uncommitted transactions
2.innodb lock waits
3.............
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

#innodb lock waits
cursor.execute("SELECT wait_started,wait_age_secs,locked_table,blocking_trx_id,blocking_pid,waiting_query FROM sys.innodb_lock_waits;")
innodb_lock_wait = cursor.fetchall()
print "\033[1;33;44m 2: result of innodb lock waits\033[0m"
if innodb_lock_wait:
    for lock_w in innodb_lock_wait:
        wait_started = lock_w[0]
        wait_age_secs = lock_w[1]
        locked_table = lock_w[2]
        blocking_trx_id = lock_w[3]
        blocking_pid = lock_w[4]
        waiting_query = lock_w[5]
        print " wait_started: %-20s  wait_age_secs: %-20s locked_table: %-20s blocking_trx_id: %-20s blocking_pid: %-20s waiting_query: %-20s" % \
              (wait_started, wait_age_secs, locked_table, blocking_trx_id, blocking_pid, waiting_query)
else:
    print "no innodb lock waits"


print '''
----------------------------------------------------------------------------------------------------------------
'''
print "\033[1;33;46m start variables check\033[0m"
#config
print '''
----------------------------------------------------------------------------------------------------------------

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



print '''
----------------------------------------------------------------------------------------------------------------
'''
print "\033[1;33;46m start innodb_buffer_pool check\033[0m"
print '''
----------------------------------------------------------------------------------------------------------------
1.innodb_buffer_pool_size                   #缓冲池大小
2.innodb_lru_scan_depth                     #控制LRU列表中可用页的数量，默认值为1024
3.innodb_buffer_pool_instances              #缓冲池实例数
4.innodb_max_dirty_pages_pct                #达到最大脏页占比，强制进行 checkpoint, 刷新一部分的脏页到磁盘
5.innodb_buffer_pool_pages_dirty            #脏页数据的大小
6.innodb_buffer_pool_pages_total            #缓冲池全部页的个数
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


print '''
----------------------------------------------------------------------------------------------------------------
'''
print "\033[1;33;46m start status check\033[0m"
print '''
----------------------------------------------------------------------------------------------------------------
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
  4). Opened_table_definitions files
  5). opend_tables
  6). Max_used_connections

----------------------------------------------------------------------------------------------------------------
'''

#1.Threads_
sql_threads_number = "show global status like '%Threads_%'"
cursor.execute(sql_threads_number)
threads_number = cursor.fetchall()
if threads_number:
    for threads in threads_number:
        threads_name = threads[0]
        threads_value = threads[1]
        print "%s : %s" % (threads_name, threads_value)

#2.Innodb_row_lock
sql_innodb_row_lock = "show global status like '%Innodb_row_lock%'"
cursor.execute(sql_innodb_row_lock)
row_lock_number = cursor.fetchall()
if row_lock_number:
    for row_lock in row_lock_number:
        row_lock_name = row_lock[0]
        row_lock_value = row_lock[1]
        print "%s : %s" % (row_lock_name, row_lock_value)


#3.opened files
sql_Opened_files = "show global status like 'Opened_files'"
cursor.execute(sql_Opened_files)
data = cursor.fetchone()
Opened_files = data[1]
print "Opened_files: %s" % Opened_files

#4.Opened_table_definitions files
sql_Opened_table_definitions = "show global status like 'Opened_table_definitions'"
cursor.execute(sql_Opened_table_definitions)
data = cursor.fetchone()
Opened_table_definitions = data[1]
print "Opened_table_definitions: %s" % Opened_table_definitions

#5.Opened_tables
sql_Opened_tables = "show global status like 'Opened_tables'"
cursor.execute(sql_Opened_tables)
data = cursor.fetchone()
Opened_tables = data[1]
print "Opened_tables: %s" % Opened_tables

#6.Max_used_connections
sql_Max_used_connections = "show global status like 'Max_used_connections'"
cursor.execute(sql_Max_used_connections)
data = cursor.fetchone()
Max_used_connections = data[1]
print "Max_used_connections: %s" % Max_used_connections


print '''
----------------------------------------------------------------------------------------------------------------
'''
print "\033[1;33;46m start database info statistics check\033[0m"
print '''
----------------------------------------------------------------------------------------------------------------
  1). total number of databases
  2). how many tables

----------------------------------------------------------------------------------------------------------------
'''
sql_all_data_statistics = "select concat(round(sum(data_length + index_length) / 1024 / 1024, 2),'M') as total_mb from information_schema.tables where TABLE_SCHEMA='niuniu_db'"
cursor.execute(sql_all_data_statistics)
all_data_statistics = cursor.fetchone()
if all_data_statistics:
    print "total number of databases: %s" % all_data_statistics

sql_tables_statistics = "SELECT COUNT( * ) FROM information_schema.tables WHERE TABLE_SCHEMA = 'niuniu_db'"
cursor.execute(sql_tables_statistics)
tables_statistics = cursor.fetchone()
if tables_statistics:
    print "total number of tables: %s" % tables_statistics


print '''
----------------------------------------------------------------------------------------------------------------
'''

print "end time: %s" % datetime.datetime.now()