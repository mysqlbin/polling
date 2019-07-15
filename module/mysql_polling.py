#!/usr/local/bin/python3
#coding=utf-8

import datetime

from common_utils.time_functions import  format_to_ymdx
from db_utils.polling_function  import get_table_schema_engine,get_version,get_table_size,get_top_big_tables,get_big_fragment_tables,\
    get_auto_increment_ratio,get_table_rows,get_table_big_column,get_table_long_varchar_column, \
    get_long_transactions,get_innodb_log_waitss,get_max_connections,get_max_used_connections,get_pages_info,get_dirty_pages_proportion,\
    get_db_reads_info,get_buffer_pool_hit,get_innodb_buffer_pool_wait_free,get_innodb_buffer_pool_pages_free,get_threads_running,get_innodb_row_lock_current_waits,\
    get_innodb_lock_waits_list

from db_utils.polling_function_index import get_too_much_columns_indexs,get_not_primary_index


if __name__ == '__main__':

    print("start time: %s" % format_to_ymdx())
    print('当前数据库版本为: {}'.format(get_version()))

    #统计表相关
    get_table_schema_engine() #对数据库实例下各个库下使用存储引擎类型的统计
    get_table_size(1)           #超过1G的大表
    get_top_big_tables(20)     #排名前20的大表
    get_big_fragment_tables('0.001')  #表碎片大于多少G才打印出来
    get_auto_increment_ratio('0.0100') #数据表的自增ID占比大于多少才打印出来, 这里是大于 1%
    get_table_rows(31132754)       #　单表超过行数多少万的表
    get_table_big_column()   #大字段列
    get_table_long_varchar_column(1000) #

    # 索引相关
    get_too_much_columns_indexs(6)
    get_not_primary_index()



    get_long_transactions(10)    #获取执行时间大于10秒的长事务






    #因 log buffer不足导致等待的次数
    get_innodb_log_waitss()

    #参数相关
    get_max_connections()
    get_max_used_connections()
    get_threads_running()

    #内存相关
    get_pages_info()
    get_dirty_pages_proportion()
    get_db_reads_info()
    get_buffer_pool_hit()
    get_innodb_buffer_pool_wait_free()
    get_innodb_buffer_pool_pages_free()


    print('Innodb_row_lock_current_waits: {} '.format(get_innodb_row_lock_current_waits()))
    get_innodb_lock_waits_list()

    print("end time: %s" % format_to_ymdx())