#!/usr/local/bin/python3
#coding=utf-8

"""
脚本需要和 pt-table-checksum一起使用
通过监控pt-table-checksum生产的checksums表来确认表是否一致
脚本要在主库执行
"""

import os,sys
import pymysql
from common_utils.time_function import format_to_ymdx


master_host = ''
master_user = ''
master_passwd = '123456abc'
master_port = 3306
master_database = 'nn_db'

slave_host = ''
slave_user = ''
slave_passwd = '123456abc'
slave_port = 3306

def mysql_query(sql, host, user, passwd, port, get_data = 1):
    try:
        conn=pymysql.connect(host=host,user=user,passwd=passwd,port=int(port),connect_timeout=5,charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql)
        if get_data == 1:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as err:
        return err

def get_process_data(sql, get_data = 1):
    results = mysql_query(sql, slave_host, slave_user, slave_passwd, slave_port, get_data)
    return results

def check_info(nowtime):

    sql = "select * from consistency_db.checksums where this_crc != master_crc and ts > '{}' ".format(nowtime)
    # 这里是连接从库
    results = get_process_data(sql, 0)
    return results

def pt_table_checksum():
    # 这里是连接主库
    cmd = "pt-table-checksum --chunk-size-limit=4.0  --nocheck-replication-filters --no-check-binlog-format --replicate=consistency_db.checksums h={},u={},p={},P={} --databases={}"\
        .format(master_host, master_user, master_passwd, master_port, master_database)
    os.system(cmd)

def pt_table_sync(format = 0):

    if format == 0:
        format = '--print'
    else:
        format = '--execute'

    cmd = " pt-table-sync --replicate=consistency_db.checksums h={},u={},p={} h={},u={},p={} {}"\
        .format(master_host, master_user, master_passwd, slave_host, slave_user, slave_passwd, format)
    os.system(cmd)


if __name__ == "__main__":

    nowtime = format_to_ymdx()

    print("start time: {}".format(nowtime))

    pt_table_checksum()

    result = check_info(nowtime)
    if result:
        for m in result:
            database = m[0]
            table =  m[1]
            print('当前{}库主从数据不一致的表为：{}'.format(database, table))

        pt_table_sync()

    print("stop time: {}".format(format_to_ymdx()))
	
