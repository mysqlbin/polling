#!/usr/local/bin/python3
#coding=utf-8

import sys
import datetime
from db_utils.db_function import get_process_data

from common_utils.time_functions import  format_to_ymdx
from db_utils.polling_table_schema  import get_table_schema_engine,get_version,get_table_size,get_top_big_tables,get_big_fragment_tables,\
    get_auto_increment_ratio,get_table_rows,get_table_big_column,get_table_long_varchar_column, get_long_transactions, get_sql_tmp_tables,get_innodb_lock_waits_list

from db_utils.polling_function_index import get_too_much_columns_indexs,get_not_primary_index


from db_utils.polling_param_status import get_param_value,get_status_value


if __name__ == '__main__':

    sql_get_user = '''select concat("\'", user, "\'", '@', "\'", host,"\'") as query from mysql.user;'''
    res = get_process_data(sql_get_user, 2)
    # print(res)
    res_user_priv = []
    for db_user in res:
        user_info = {}
        sql_get_permission = 'show grants for {};'.format(db_user[0])
        user_priv = get_process_data(sql_get_permission, 2)
        user_info['user'] = db_user[0]
        user_info['privileges'] = user_priv
        res_user_priv.append(user_info)


    for db_user in res_user_priv:
        # print(db_user['user'])
        print('User@Host: '.format(db_user['user']))
        print('privileges: ')
        for pri in db_user['privileges']:
            print(  pri[0])
    sys.exit()


    print("start time: %s" % format_to_ymdx())

    print('当前数据库版本为: {}'.format(get_version()))

    print("\033[1;33;44m 一、统计表相关: \033[0m")
    get_table_schema_engine() #对数据库实例下各个库下使用存储引擎类型的统计
    get_table_size(1)           #超过1G的大表
    get_top_big_tables(20)     #排名前20的大表
    get_big_fragment_tables('0.001')  #表碎片大于多少G才打印出来
    get_auto_increment_ratio('0.0100') #数据表的自增ID占比大于多少才打印出来, 这里是大于 1%
    get_table_rows(31132754)       #　单表超过行数多少万的表
    get_table_big_column()   #大字段列
    get_table_long_varchar_column(1000)


    print("\033[1;33;44m 二、索引检查: \033[0m")
    get_too_much_columns_indexs(6)
    get_not_primary_index()

    print("\033[1;33;44m 三、参数: \033[0m")
    print("\033[1;33;44m 3.1.1--InnoDB层参数: \033[0m")
    get_param_value('tx_isolation')
    get_param_value('innodb_rollback_on_timeout')
    get_param_value('innodb_io_capacity')
    get_param_value('innodb_io_capacity_max')
    get_param_value('innodb_flush_method')
    get_param_value('innodb_file_per_table')
    get_param_value('innodb_open_files')
    get_param_value('innodb_data_home_dir')
    get_param_value('innodb_lock_wait_timeout')
    get_param_value('innodb_thread_concurrency')
    get_param_value('innodb_fast_shutdown')
    get_param_value('innodb_data_file_path')
    get_param_value('innodb_write_io_threads')
    get_param_value('innodb_read_io_threads')
    get_param_value('innodb_purge_threads')
    get_param_value('innodb_page_cleaners')
    get_param_value('innodb_doublewrite')
    get_param_value('innodb_change_buffer_max_size')
    get_param_value('innodb_change_buffering')
    get_param_value('innodb_adaptive_hash_index')

    print("\033[1;33;44m 3.1.2--InnoDB redo参数: \033[0m")
    get_param_value('innodb_flush_log_at_trx_commit')
    get_param_value('innodb_log_file_size')
    get_param_value('innodb_log_files_in_group')
    get_param_value('innodb_log_buffer_size')

    print("\033[1;33;44m 3.1.3--InnoDB undo参数: \033[0m")

    print("\033[1;33;44m 3.2--server层参数: \033[0m")
    print("\033[1;33;44m 3.2.1--binlog相关的参数: \033[0m")
    get_param_value('sync_binlog')
    get_param_value('binlog_format')
    get_param_value('max_binlog_size')
    get_param_value('max_binlog_cache_size')
    get_param_value('expire_logs_days')
    get_param_value('binlog_cache_size')

    print("\033[1;33;44m 3.2.2--线程/会话相关的内存参数: \033[0m")
    get_param_value('key_buffer_size')
    get_param_value('query_cache_size')
    get_param_value('read_buffer_size')
    get_param_value('read_rnd_buffer_size')
    get_param_value('sort_buffer_size')
    get_param_value('join_buffer_size')
    get_param_value('binlog_cache_size')
    get_param_value('tmp_table_size')

    print("\033[1;33;44m 3.2.4--其它的参数: \033[0m")
    get_param_value('max_allowed_packet')
    get_param_value('table_open_cache')
    get_param_value('max_execution_time')
    get_param_value('sql_mode')
    get_param_value('interactive_timeout')
    get_param_value('wait_timeout')
    get_param_value('open_files_limit')
    get_param_value('lower_case_table_names')
    get_param_value('slow_query_log')
    get_param_value('long_query_time')
    get_param_value('log_queries_not_using_indexes')
    get_param_value('system_time_zone')
    get_param_value('time_zone')
    get_param_value('log_timestamps')

    print("\033[1;33;44m 数据库连接数: \033[0m")
    get_param_value('max_connections')
    get_param_value('max_connect_errors')
    get_param_value('max_user_connections')
    get_status_value('Max_used_connections')


    print("\033[1;33;44m 四、InnoDB Buffer Pool的使用状况: \033[0m")
    print("\033[1;33;44m 4.1--ibp的参数: \033[0m")
    get_param_value('innodb_random_read_ahead')
    get_param_value('innodb_read_ahead_threshold')
    get_param_value('innodb_buffer_pool_load_at_startup')
    get_param_value('innodb_buffer_pool_dump_at_shutdown')
    get_param_value('innodb_flush_neighbors')
    get_param_value('innodb_buffer_pool_size')
    get_param_value('innodb_buffer_pool_instances')
    get_param_value('innodb_lru_scan_depth')
    get_param_value('innodb_max_dirty_pages_pct')
    get_param_value('innodb_old_blocks_pct')
    get_param_value('innodb_old_blocks_time')

    print("\033[1;33;44m 4.2--ibp的状态: \033[0m")
    get_status_value('innodb_buffer_pool_pages_dirty')
    get_status_value('innodb_buffer_pool_pages_total')
    get_status_value('Innodb_buffer_pool_pages_data')
    get_status_value('innodb_buffer_pool_read_requests')
    get_status_value('innodb_buffer_pool_read_ahead')
    get_status_value('innodb_buffer_pool_reads')
    get_status_value('Innodb_buffer_pool_pages_free')
    get_status_value('Innodb_buffer_pool_wait_free')

    print("\033[1;33;44m 4.3--脏页在内存中的占比: \033[0m")
    ibp_pages_dirty = get_status_value('innodb_buffer_pool_pages_dirty', 0)
    ibp_pages_total = get_status_value('innodb_buffer_pool_pages_total', 0)
    dirty_page = round(int(ibp_pages_dirty) / int(ibp_pages_total), 4)
    print('脏页在内存数据页中的占比为: {}%'.format(dirty_page * 100))

    print("\033[1;33;44m 4.4--InnoDB buffer pool 命中率: \033[0m")
    ibp_read_requests = get_status_value('innodb_buffer_pool_read_requests', 0)
    ibp_read_ahead    = get_status_value('innodb_buffer_pool_read_ahead', 0)
    ibp_read_reads    = get_status_value('innodb_buffer_pool_reads', 0)
    ibp_hit = int(ibp_read_requests) / (int(ibp_read_requests) + int(ibp_read_ahead) + int(ibp_read_reads))
    print('InnoDB buffer pool 命中率: {}%'.format(round(ibp_hit,4) * 100))

    print("\033[1;33;44m 4.5--ibp是否使用紧张: \033[0m")
    ibp_wait_free = get_status_value('Innodb_buffer_pool_wait_free', 0)
    if int(ibp_wait_free) > 0:
        print('注意：InnoDB Buffer Pool可能不够用了，需要详细检查并处理，目前等待申请空闲列表的次数为: {} 次'.format(ibp_wait_free))




    print("\033[1;33;44m 五、MySQL状态值: \033[0m")


    print("\033[1;33;44m 5.1--并发线程连接数: \033[0m")
    get_status_value('Threads_connected')
    get_status_value('Threads_created')
    get_status_value('Threads_running')

    print("\033[1;33;44m 5.2--行锁等待: \033[0m")
    get_status_value('Innodb_row_lock_current_waits')
    get_status_value('Innodb_row_lock_time')
    get_status_value('Innodb_row_lock_time_avg')
    get_status_value('Innodb_row_lock_time_max')
    get_status_value('Innodb_row_lock_waits')

    print("\033[1;33;44m 5.3--打开表的次数: \033[0m")
    get_status_value('Open_files')
    get_status_value('Open_tables')
    get_status_value('Opened_tables')

    print("\033[1;33;44m 5.4--创建的内存临时表和磁盘临时表的次数: \033[0m")
    get_status_value('Created_tmp_tables')
    get_status_value('Created_tmp_disk_tables')

    print("\033[1;33;44m 5.5--double write的使用情况: \033[0m")
    get_status_value('Innodb_dblwr_pages_written')
    get_status_value('Innodb_dblwr_writes')

    dblwr_pages_written = get_status_value('Innodb_dblwr_pages_written', 0)
    dblwr_writes        = get_status_value('Innodb_dblwr_writes', 0)
    merge_pages         = int(dblwr_pages_written) / int(dblwr_writes)
    print('每次写操作合并page的个数: {}'.format(round(merge_pages, 0)))

    print("\033[1;33;44m 5.6--因log buffer不足导致等待的次数: \033[0m")
    get_status_value('Innodb_log_waits')
    innodb_log_waits = get_status_value('Innodb_log_waits', 0)
    print('因 log buffer不足导致等待的次数(Innodb_log_waits): {} 次'.format(innodb_log_waits))


    get_long_transactions(10)    #获取执行时间大于10秒的长事务
    get_sql_tmp_tables(2)         #使用到内存临时表或者磁盘临时表的SQL
    get_innodb_lock_waits_list()  #行锁等待列表



    print("end time: %s" % format_to_ymdx())