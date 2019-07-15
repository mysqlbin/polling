#!/usr/local/bin/python3
#coding=utf-8

from db_utils.db_function import get_process_data

#0. too much columns indexes
def get_too_much_columns_indexs(index_count = 5):

    print("\033[1;33;44m 0: result of to much columns indexes\033[0m")
    sql = "select s.table_schema,s.table_name,s.index_name,s.column_name from information_schema.STATISTICS s, \
          (select table_name,index_name,count(*) from information_schema.STATISTICS where table_schema not in \
          ('information_schema','performance_schema','mysql','sys') group by table_name,index_name having \
          count(*)> {})t where s.table_name=t.table_name and s.index_name=t.index_name;" .format(index_count)
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('table_schema:{:15s}  table_name:{:30s} index_name:{:20s} column_name:{:20s} '.format(val[0], val[1], val[2], val[3]))
    else:
        print( "all index have column under {}".format(index_count))


# 1. talbe not has primary index
def get_not_primary_index():

    print("\033[1;33;44m 1: result of table has not primary indexes\033[0m")
    sql = "SELECT t.table_schema,t.table_name FROM information_schema.tables AS t LEFT JOIN   \
        (SELECT DISTINCT table_schema, table_name FROM information_schema.`KEY_COLUMN_USAGE` ) AS kt ON \
        kt.table_schema=t.table_schema AND kt.table_name = t.table_name WHERE t.table_schema NOT IN \
        ('mysql', 'information_schema', 'performance_schema', 'sys') AND kt.table_name IS NULL;"

    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('table_schema:{:15s}  table_name:{:30s} '.format(val[0], val[1]))
    else:
        print("all tables have indexes")
