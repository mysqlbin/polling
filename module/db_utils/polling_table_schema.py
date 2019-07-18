#!/usr/local/bin/python3
#coding=utf-8

from db_utils.db_function import get_process_data

#0 get table schema engine
def get_table_schema_engine():
    print("\033[1;33;44m 0: result of group by engine type: \033[0m")
    sql = "select table_schema, engine, count(*) as engine_counts from information_schema.tables where table_schema not in \
           ('information_schema','mysql','performance_schema','sys') group by table_schema,engine;"
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('table_schema:{:15s}  engine:{:30s} engine_counts:{:15} '.format(val[0], val[1], val[2]))

#1 get tables more than 10G
def get_table_size(val = 1):
    print("\033[1;33;44m 1: result of table is more than 1G\033[0m")
    sql = "select table_schema,table_name,concat(round((data_length+index_length)/1024/1024,2),'M') as size, round((data_length+index_length)/1024/1024,2) as data FROM \
        information_schema.tables where (DATA_LENGTH+INDEX_LENGTH) > {}*1024*1024*1024  and table_schema not in \
        ('information_schema','mysql','performance_schema','sys') order by size desc".format(val)
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('table_schema:{:15s}  table_name:{:30s} size:{:10s}'.format(val[0], val[1], val[2]))
    else:
        print("no table is more than 1G...")


#2 get the top 20 tables
def get_top_big_tables(limit = 20):
    print("\033[1;33;44m 2: result of the top tables\033[0m")
    sql = "SELECT table_schema,table_name,concat(round(data_length/1024/1024,2),'M') AS data_mb,concat(round(index_length/1024/1024,2), 'M') AS index_mb, \
                            concat(round((data_length + index_length)/1024/1024,2), 'M') AS all_mb,table_rows FROM \
                            information_schema.tables  where table_schema not in ('information_schema','mysql','performance_schema','sys') order by all_mb desc limit {}".format(limit)
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('table_schema:{:15s}  table_name:{:30s} all_size:{:15s} data_size:{:15s} index_size:{:15s} table_rows:{:5}'.format(val[0], val[1], val[2], val[3], val[4], val[5]))
    else:
        print("no tabls the top...")

#3 get tables which have big fragment
def get_big_fragment_tables(data_free = '0.1'):
    print("\033[1;33;44m 3: result of table has big fragment\033[0m")
    sql = "select table_schema,table_name,concat(round(DATA_FREE/1024/1024,2),'M') from information_schema.TABLES where table_schema not in \
          ('information_schema','mysql','performance_schema','sys') and data_free > {} *1024*1024*1024 order by DATA_FREE desc".format(data_free)
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('table_schema:{:15s}  table_name:{:30s} fragment:{:10s}'. format(val[0], val[1], val[2]))
    else:
        print("no table has big fragment...")

#4 auto increment ratio
def get_auto_increment_ratio(auto_increment_ratio = '0.3000'):

    print("\033[1;33;44m 4: result of auto increment ratio\033[0m")
    sql = "select table_schema,table_name,auto_increment_ratio,max_value,auto_increment from sys.schema_auto_increment_columns \
          where auto_increment_ratio > {} and table_schema not in \
          ('information_schema','mysql','performance_schema','sys') order by auto_increment_ratio desc".format(auto_increment_ratio)
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('table_schema:{:15s} table_name:{:30s} auto_increment_ratio:{} max_value:{} auto_increment:{}'.format(val[0], val[1], val[2], val[3], val[4]))
    else:
        print("no table auto increment ratio has more than {}...".format(auto_increment_ratio))

#5 get table rows
def get_table_rows(table_rows = 20000000):
    print("\033[1;33;44m 5: result of table has more than {}\033[0m".format(table_rows))
    sql = "select table_schema,table_name,table_rows from \
         information_schema.TABLES where table_schema not in ('information_schema','mysql','performance_schema','sys') \
         and table_rows > {} order by table_rows desc;".format(table_rows)

    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('table_schema:{:15} table_name:{:30s} table_rows:{} '.format(val[0], val[1], val[2]))
    else:
        print("no table has has more than {} rows...".format(table_rows))

# 6.get tables which have big columns
def get_table_big_column():
    print("\033[1;33;44m 6: result of table has big columns\033[0m")
    sql = "select table_schema,table_name,column_name,data_type from information_schema.columns where data_type in \
          ('blob','clob','text','medium text','long text') and table_schema not in \
          ('information_schema','performance_schema','mysql','sys')"
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            print('table_schema:{:15} table_name:{:30s} column_name:{:30s} data_type:{:20s}'.format(val[0], val[1], val[2], val[3]))
    else:
        print("no table has has big columns")

# 7.get tables which have long varchar columns
def get_table_long_varchar_column(character_maximum_length = 500):

    print("\033[1;33;44m 7: result of table has long columns\033[0m")
    sql="select table_schema,table_name,column_name,data_type,CHARACTER_MAXIMUM_LENGTH from information_schema.columns \
    where DATA_TYPE='varchar' and CHARACTER_MAXIMUM_LENGTH > {} and table_schema not in \
    ('information_schema','performance_schema','mysql','sys');".format(character_maximum_length)
    results = get_process_data(sql, 0)

    if results:
        for val in results:
            print('table_schema:{:15} table_name:{:30s} column_name:{:30s} data_type:{:20s} CHARACTER_MAXIMUM_LENGTH:{:20}'.format(val[0], val[1], val[2], val[3], val[4]))
    else:
        print("no table has long columns")

#long uncommitted transactions
def get_long_transactions(time = 1):
    print("\033[1;33;44m result of long uncommitted transactions\033[0m")
    sql = "select pro.host, pro.user, pro.db, trx.trx_state, pro.COMMAND, concat(pro.time,'s') as runtime, trx.trx_id, pro.id as thread_id, trx.trx_query \
          from  information_schema.innodb_trx trx left join information_schema.PROCESSLIST pro on trx.trx_mysql_thread_id = pro.id where pro.time > {}".format(time)
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            if val[8] == None:
                trx_query = ''
            else:
                trx_query = val[0]
            print('host:{:20s} user:{:20s} db:{:20s} trx_state:{:10s} command:{:10s} time:{:10s} trx_id:{:10s} thread_id:{}  trx_query:{:20s} '.format(val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], trx_query))
    else:
        print("   no long uncommitted transactions...")

#tmp_tables, tmp_disk_tables
def get_sql_tmp_tables(limit = 20):
    print("\033[1;33;44m result of sql tmp tables count\033[0m")
    sql = "select db, tmp_tables, tmp_disk_tables, tmp_tables+tmp_disk_tables as tmp_all, query from sys.statement_analysis \
          where tmp_tables>0 or tmp_disk_tables >0 order by tmp_all desc limit {};".format(limit)
    results = get_process_data(sql, 0)
    if results:
        for val in results:
            if val[0] == None:
                db_name = ''
            else:
                db_name = val[0]
            print('db_name:{:20s} tmp_tables:{} tmp_disk_tables:{} tmp_all:{} query_sql:{}'.format(db_name, val[1], val[2], val[3], val[4]))
    else:
        print("no tmp tables data")


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

        print("\033[1;33;44m 行锁等待列表：\033[0m")

        sql_version = "select version()"
        results = get_process_data(sql_version)
        if results:
            get_version = results[0][0:3].replace('.','')
        else:
            get_version = '57'

        if get_version >= '57':
            print(1)
            sql  = "select locked_index,locked_type,blocking_lock_mode,waiting_lock_mode,waiting_query from sys.innodb_lock_waits"
            results = get_process_data(sql, 0)
            if results:
                for val in results:
                    print('locked_index:{:10s} locked_type:{:10s} blocking_block_mode:{:10s} waiting_lock_mode:{:10s} waiting_query:{}'.format(val[0], val[1], val[2], val[3], val[4]))
            else:
                print("no innodb row lock current waits list...")
        else:
            sql = "select requesting_trx_id,requested_lock_id,blocking_trx_id,blocking_lock_id from information_schema.innodb_lock_waits"
            results = get_process_data(sql, 0)
            if results:
                for val in results:
                    print('requesting_trx_id:{:10s} requested_lock_id:{:10s} blocking_trx_id:{:10s} blocking_lock_id:{} '.format(val[0], val[1], val[2], val[3]))
            else:
                print("no innodb row lock current waits list...")


def get_instance_user_privileges():
    sql_get_user = '''select concat("\'", user, "\'", '@', "\'", host,"\'") as query from mysql.user;'''
    res = get_process_data(sql_get_user, 2)
    res_user_priv = []
    for db_user in res:
        user_info = {}
        sql_get_permission = 'show grants for {};'.format(db_user[0])
        user_priv = get_process_data(sql_get_permission, 2)
        user_info['user'] = db_user[0]
        user_info['privileges'] = user_priv
        res_user_priv.append(user_info)
    return res_user_priv


