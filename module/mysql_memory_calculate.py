#!/usr/local/bin/python3
#coding=utf-8

import datetime


from common_utils.calculator import  byte_to_mb
from db_utils.polling_function  import get_innodb_buffer_pool_size,get_innodb_log_buffer_size,get_key_buffer_size,\
    get_query_cache_size,get_read_buffer_size,get_read_rnd_buffer_size,get_sort_buffer_size,get_join_buffer_size,\
    get_binlog_cache_size,get_tmp_table_size,get_threads_running

if __name__ == '__main__':

    global_buffers  = int(get_innodb_buffer_pool_size())+int(get_innodb_log_buffer_size())+int(get_key_buffer_size())+int(get_query_cache_size())
    threads_buffers = int(get_read_buffer_size()) + int(get_read_rnd_buffer_size()) + int(get_sort_buffer_size()) + int(get_join_buffer_size()) + int(get_binlog_cache_size()) + int(get_tmp_table_size())
    threads_running = int(get_threads_running())
    all_threads_buffers = threads_buffers * 4
    mysql_memory_used = byte_to_mb(global_buffers + all_threads_buffers)
    print(global_buffers)
    print(threads_buffers)
    print(threads_running)
    print(mysql_memory_used)

    #1136!=1638