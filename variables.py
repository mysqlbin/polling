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
start table check
1.size
2.much indexes
3.fragment
4.rows
5.charset
6.big column
7.long column

----------------------------------------------------------------------------------------------------------------
'''
#get tables more than 10G
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

#get tables which have more than 6 indexes
cursor.execute("select t1.name,t2.num from information_schema.innodb_sys_tables t1, (select table_id,count(*) as num from \
information_schema.innodb_sys_indexes group by table_id having count(*) >=6) t2 where t1.table_id =t2.table_id")
table_index = cursor.fetchall()

print "\033[1;33;44m 2: result of table more than 6 indexes\033[0m"
if table_index:
    for table in table_index:
        table_name = table[0]
        index_num = table[1]
        print " table_name: %-50s  index_num: %10d " % \
              (table_name, index_num)
else:
    print "no table has more than 6 indexes"


#get tables which have big fragment
cursor.execute("select table_schema,table_name,DATA_FREE from \
information_schema.TABLES where table_schema not in ('information_schema','mysql','performance_schema','sys') \
and data_free > 1*1024*1024*1024 order by DATA_FREE desc;")
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

#get tables which have 20000000 rows
cursor.execute("select table_schema,table_name,table_rows from \
information_schema.TABLES where table_schema not in ('information_schema','mysql','performance_schema','sys') \
and table_rows > 20000000 order by table_rows desc;")
table_fragment = cursor.fetchall()

print "\033[1;33;44m 4: result of table has more than 20000000 rows\033[0m"
if table_fragment:
    for table in table_fragment:
        table_schema = table[0]
        table_name = table[1]
        table_rows = table[2]
        print " table_schema: %-20s  table_name : %-20s table_rows: %10d " % \
              (table_schema, table_name, table_rows)
else:
    print "no table has has more than 20000000 rows"

#get table charset not default
cursor.execute("show variables like 'character_set_server';")
default_charset = str(cursor.fetchone()[1])
default_charset = default_charset+"_general_ci"
sql = "select table_schema,table_name,table_collation from information_schema.tables where table_schema not \
in ('information_schema','mysql','performance_schema','sys') and table_collation !='"+default_charset+"';"
cursor.execute(sql)
table_charset = cursor.fetchall()

print "\033[1;33;44m 5: result of table is not in default charset\033[0m"
if table_charset:
    for table in table_charset:
        table_schema = table[0]
        table_name = table[1]
        charset = table[2]
        print " table_schema: %-20s  table_name : %-20s charset: %10s " % \
              (table_schema, table_name, charset)
else:
    print "no table is not in default charset"

#get tables which have big columns
cursor.execute("select table_schema,table_name,column_name,data_type from information_schema.columns where data_type in \
('blob','clob','text','medium text','long text') and table_schema not in \
('information_schema','performance_schema','mysql','sys')")
table_big_cols = cursor.fetchall()

print "\033[1;33;44m 6: result of table has big columns\033[0m"
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

#get tables which have long varchar columns
cursor.execute("select table_schema,table_name,column_name,data_type,CHARACTER_MAXIMUM_LENGTH from information_schema.columns \
where DATA_TYPE='varchar' and CHARACTER_MAXIMUM_LENGTH > 500 and table_schema not in \
('information_schema','performance_schema','mysql','sys');")
table_long_cols = cursor.fetchall()

print "\033[1;33;44m 7: result of table has long columns\033[0m"
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



# index check
print '''
----------------------------------------------------------------------------------------------------------------
start index check
1.get tables which have not indexes
2.redundant indexes
3.to much columns indexes
4.unused indexes
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


# #unused indexes
# cursor.execute("select * from sys.schema_unused_indexes;")
# unused_indexes = cursor.fetchall()
#
# print "\033[1;33;44m 4: result of redundant indexes\033[0m"
# if unused_indexes:
#     for index in unused_indexes:
#         table_schema = index[0]
#         table_name = index[1]
#         index_name = index[2]
#         print " table_schema: %-20s  table_name: %-20s index_name: %-20s" % \
#               (table_schema, table_name, index_name)
# else:
#     print "no unused indexes"
