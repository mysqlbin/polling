#!/usr/local/bin/python3
#coding=utf-8

from db_utils.db_function import get_process_data

#get tables more than 10G
def get_table_size():
    print("\033[1;33;44m 1: result of table is more than 1G\033[0m")
    sql = "select table_schema,table_name,concat(round((data_length+index_length)/1024/1024,2),'M') as size, round((data_length+index_length)/1024/1024,2) as data FROM \
        information_schema.tables where (DATA_LENGTH+INDEX_LENGTH) > 1*1024*1024*1024  and table_schema not in \
        ('information_schema','mysql','performance_schema','sys') order by size desc"
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('table_schema:{:15s}  table_name:{:30s} size:{:10s}'.format(val[0], val[1], val[2]))
    else:
        print("no table is more than 1G...")


#get the top 20 tables
def get_top20_big_tables():
    print("\033[1;33;44m 2: result of the top 20 tables\033[0m")
    sql = "SELECT table_schema,table_name,concat(round(data_length/1024/1024,2),'M') AS data_mb,concat(round(index_length/1024/1024,2), 'M') AS index_mb, \
                            concat(round((data_length + index_length)/1024/1024,2), 'M') AS all_mb,table_rows FROM \
                            information_schema.tables  where table_schema not in ('information_schema','mysql','performance_schema','sys') order by all_mb desc limit 20"
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('table_schema:{:15s}  table_name:{:30s} all_size:{:15s} data_size:{:15s} index_size:{:15s} table_rows:{:5}'.format(val[0], val[1], val[2], val[3], val[4], val[5]))
    else:
        print("no tabls the top 20...")

#get tables which have big fragment
def get_big_fragment_tables():
    print("\033[1;33;44m 3: result of table has big fragment\033[0m")
    sql = "select table_schema,table_name,concat(round(DATA_FREE/1024/1024,2),'M') from information_schema.TABLES where table_schema not in \
          ('information_schema','mysql','performance_schema','sys') and data_free > 0.0*1024*1024*1024 order by DATA_FREE desc"
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('table_schema:{:15s}  table_name:{:30s} fragment:{:10s}'. format(val[0], val[1], val[2]))
    else:
        print("no table has big fragment...")

#auto increment ratio
def get_auto_increment_ratio():
    #if sys.argv[1] == '5.7':
    print("\033[1;33;44m 4: result of auto increment ratio\033[0m")
    sql = "select table_schema,table_name,auto_increment_ratio,max_value,auto_increment from sys.schema_auto_increment_columns \
          where auto_increment_ratio > '0.00001' and table_schema not in \
          ('information_schema','mysql','performance_schema','sys') order by auto_increment_ratio desc"
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('table_schema:{:15s} table_name:{:30s} auto_increment_ratio:{} max_value:{} auto_increment:{}'.format(val[0], val[1], val[2], val[3], val[4]))
    else:
        print("no table auto increment ratio has more than 50%...")

#long uncommitted transactions
def get_long_uncommitted_transactions():
    print("\033[1;33;44m 1: result of long uncommitted transactions\033[0m")
    sql = "select b.host, b.user, b.db, a. trx_state,  b.COMMAND, concat(b.time,'s'), a.trx_id from  \
          information_schema.innodb_trx a left join information_schema.PROCESSLIST b on a.trx_mysql_thread_id = b.id"
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('host:{:20s} user:{:20s} db:{:20s} trx_state:{:10s} command:{:10s} time:{:10s} trx_id:{} '.format(val[0], val[1], val[2], val[3], val[4], val[5], val[6]))
    else:
        print("no long uncommitted transactions...")


def get_innodb_log_waitss():
    sql = "show global status like 'Innodb_log_waits'"
    results = get_process_data(sql)
    if results:
        print('因 log buffer不足导致等待的次数(Innodb_log_waits): {} 次'.format(results[1]))

def get_max_connections():
    sql = "show global status like 'max_connections'"
    results = get_process_data(sql)
    if results:
        print('max_connections: {} '.format(results[1]))

def get_max_used_connections():
    sql = "show global status like 'Max_used_connections'"
    results = get_process_data(sql)
    if results:
        print('Max_used_connections: {} '.format(results[1]))


def get_innodb_buffer_pool_pages_dirty():
    sql = "show global status like 'innodb_buffer_pool_pages_dirty'"
    results = get_process_data(sql)
    if results:
        return results[1]

def get_innodb_buffer_pool_pages_total():
    sql = "show global status like 'innodb_buffer_pool_pages_total'"
    results = get_process_data(sql)
    if results:
        return results[1]

def get_pages_info():
    print('innodb_buffer_pool_pages_dirty: {} '.format(get_innodb_buffer_pool_pages_dirty()))
    print('innodb_buffer_pool_pages_total: {} '.format(get_innodb_buffer_pool_pages_total()))

def get_dirty_pages_proportion():
    proportion = (round(int(get_innodb_buffer_pool_pages_dirty()) / int(get_innodb_buffer_pool_pages_total()),4)) * 100
    print('脏页占比: {}%'.format(proportion))


def get_innodb_buffer_pool_read_requests():
    sql = "show global status like 'innodb_buffer_pool_read_requests'"
    results = get_process_data(sql)
    if results:
        return results[1]

def get_innodb_buffer_pool_read_ahead():
    sql = "show global status like 'innodb_buffer_pool_read_ahead'"
    results = get_process_data(sql)
    if results:
        return results[1]

def get_innodb_buffer_pool_reads():
    sql = "show global status like 'innodb_buffer_pool_reads'"
    results = get_process_data(sql)
    if results:
        return results[1]

def get_db_reads_info():
    print('innodb_buffer_pool_read_requests: {} '.format(get_innodb_buffer_pool_read_requests()))
    print('innodb_buffer_pool_read_ahead: {} '.format(get_innodb_buffer_pool_read_ahead()))
    print('innodb_buffer_pool_reads: {} '.format(get_innodb_buffer_pool_reads()))

def get_buffer_pool_hit():
    proportion = (round(int(get_innodb_buffer_pool_read_requests()) / (int(get_innodb_buffer_pool_read_requests()) + int(get_innodb_buffer_pool_read_ahead()) + int(get_innodb_buffer_pool_reads())),2)) *100
    print('InnoDB buffer pool 命中率: {}%'.format(proportion))

def get_innodb_buffer_pool_wait_free():
    sql = "show global status like 'Innodb_buffer_pool_wait_free'"
    results = get_process_data(sql)
    if results:
        print('Innodb_buffer_pool_wait_free: {} '.format(results[1]))

def get_innodb_buffer_pool_pages_free():
    sql = "show global status like 'Innodb_buffer_pool_pages_free'"
    results = get_process_data(sql)
    if results:
        print('Innodb_buffer_pool_pages_free: {} '.format(results[1]))

def get_threads_running():
    sql = "show global status like 'Threads_running'"
    results = get_process_data(sql)
    if results:
        print('Threads_running: {} '.format(results[1]))

def get_version():
    sql = "select version()"
    results = get_process_data(sql)
    if results:
        return results[0]

def get_innodb_row_lock_current_waits():
    sql = "show global status like 'Innodb_row_lock_current_waits'"
    results = get_process_data(sql)
    if results:
        return results[1]

def get_innodb_lock_waits_list():

    innodb_row_lock_current_waits = get_innodb_row_lock_current_waits()
    if int(innodb_row_lock_current_waits) > 0:
        print("\033[1;33;44m 1: result of innodb row lock current waits\033[0m")

        sql_version = "select version()"
        results = get_process_data(sql_version)
        if results:
            get_version = results[0][0:3]
        else:
            get_version = '5.7'
        if get_version >= '5.7':

            sql  = "SELECT locked_index,locked_type,blocking_lock_mode,waiting_lock_mode,waiting_query FROM sys.innodb_lock_waits"
            results = get_process_data(sql, 0)
            if results:
                for val in results:
                    print('locked_index:{:10s} locked_type:{:10s} blockint_block_mode:{:10s} waiting_lock_mode:{:10s} waiting_query:{}'.format(val[0], val[1], val[2], val[3], val[4]))
            else:
                print("no innodb row lock current waits...")
        else:
            sql = "select requesting_trx_id,requested_lock_id,blocking_trx_id,blocking_lock_id from information_schema.INNODB_LOCK_WAITS"
            results = get_process_data(sql, 0)
            if results:
                for val in results:
                    print('requesting_trx_id:{:10s} requested_lock_id:{:10s} blocking_trx_id:{:10s} blocking_lock_id:{} '.format(val[0], val[1], val[2], val[3]))
            else:
                print("no innodb row lock current waits...")



def get_innodb_buffer_pool_size():
    sql = "show global variables like 'innodb_buffer_pool_size'"
    results = get_process_data(sql)
    if results:
        return results[1]


def get_innodb_log_buffer_size():
    sql = "show global variables like 'innodb_log_buffer_size'"
    results = get_process_data(sql)
    if results:
        return results[1]


def get_key_buffer_size():
    sql = "show global variables like 'key_buffer_size'"
    results = get_process_data(sql)
    if results:
        return results[1]


def get_query_cache_size():
    sql = "show global variables like 'query_cache_size'"
    results = get_process_data(sql)
    if results:
        return results[1]



def get_read_buffer_size():
    sql = "show global variables like 'read_buffer_size'"
    results = get_process_data(sql)
    if results:
        return results[1]


def get_read_rnd_buffer_size():
    sql = "show global variables like 'read_rnd_buffer_size'"
    results = get_process_data(sql)
    if results:
        return results[1]


def get_read_rnd_buffer_size():
    sql = "show global variables like 'read_rnd_buffer_size'"
    results = get_process_data(sql)
    if results:
        return results[1]

def get_sort_buffer_size():
    sql = "show global variables like 'sort_buffer_size'"
    results = get_process_data(sql)
    if results:
        return results[1]



def get_join_buffer_size():
    sql = "show global variables like 'join_buffer_size'"
    results = get_process_data(sql)
    if results:
        return results[1]

def get_binlog_cache_size():
    sql = "show global variables like 'binlog_cache_size'"
    results = get_process_data(sql)
    if results:
        return results[1]

def get_tmp_table_size():
    sql = "show global variables like 'tmp_table_size'"
    results = get_process_data(sql)
    if results:
        return results[1]

def get_threads_running():
    sql = "show status like 'Threads_running'"
    results = get_process_data(sql)
    if results:
        return results[1]
