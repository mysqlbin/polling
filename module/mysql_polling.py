#!/usr/local/bin/python3
#coding=utf-8

import datetime

from common_utils.time_function import  format_to_ymdx
from db_utils.polling_function  import get_version,get_table_size,get_top20_big_tables,get_big_fragment_tables,get_auto_increment_ratio,\
    get_long_uncommitted_transactions,get_innodb_log_waitss,get_max_connections,get_max_used_connections,get_pages_info,get_dirty_pages_proportion,\
    get_db_reads_info,get_buffer_pool_hit,get_innodb_buffer_pool_wait_free,get_innodb_buffer_pool_pages_free,get_threads_running,get_innodb_row_lock_current_waits,\
    get_innodb_lock_waits_list


if __name__ == '__main__':

    print("start time: %s" % format_to_ymdx())
    print('当前数据库版本为: {}'.format(get_version()))

    get_table_size()
    get_top20_big_tables()
    get_big_fragment_tables()
    get_auto_increment_ratio()
    get_long_uncommitted_transactions()
    get_innodb_log_waitss()
    get_max_connections()
    get_max_used_connections()
    get_pages_info()
    get_dirty_pages_proportion()
    get_db_reads_info()
    get_buffer_pool_hit()
    get_innodb_buffer_pool_wait_free()
    get_innodb_buffer_pool_pages_free()
    get_threads_running()

    print('Innodb_row_lock_current_waits: {} '.format(get_innodb_row_lock_current_waits()))
    get_innodb_lock_waits_list()

    print("end time: %s" % format_to_ymdx())