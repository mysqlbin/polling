#!/usr/local/bin/python3
#coding=utf-8

"""
脚本需要和 pt-table-checksum一起使用
通过监控pt-table-checksum生产的checksums表来确认表是否一致
脚本要在主库执行
"""


# import smtplib
# from email.mime.text import MIMEText
import time,datetime
import os,sys
import pymysql
from functions import format_time

# from dingtalkchatbot.chatbot import DingtalkChatbot


# webhook = 'https://oapi.dingtalk.com/robot/send?access_token=1f077306f882465984c4d9932afca61d6b85310093cda55bd14993a84f50446b'
# xiaoding = DingtalkChatbot(webhook)

master_host = ''
master_user = 'pt_user'
master_passwd = ''
master_port = 3306
master_database = ''

slave_host = ''
slave_user = 'pt_user'
slave_passwd = ''
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

def pt_table_sync(algorithms = 0):

    if algorithms == 0:
        algorithms = '--print'
    else:
        algorithms = '--execute'

    cmd = " pt-table-sync --replicate=consistency_db.checksums h={},u={},p={} h={},u={},p={} {}"\
        .format(master_host, master_user, master_passwd, slave_host, slave_user, slave_passwd, algorithms)
    os.system(cmd)


if __name__ == "__main__":

    nowtime = time.strftime('%Y-%m-%d %X', time.localtime())

    pt_table_checksum()

    result = check_info(nowtime)
    if result:
        for m in result:
            database = m[0]
            table =  m[1]
            print('当前{}库主从数据不一致的表为：{}'.format(database, table))

        pt_table_sync()


    """
	pt-table-sync --replicate=consistency_db.checksums h=192.168.1.10,u=pt_user,p=11 h=192.168.1.11,u=pt_user,p=11 --print
	
	REPLACE INTO `niuniu_db`.`table_clubgamescoredetail`(`id`, `nclubid`, `ntableid`, `nchairid`, `sztoken`, `nround`, `nbasescore`, `nplaycount`, `tstarttime`, `tendtime`, `nplayerid`, `brobot`, `szcarddata`, `nenterscore`, `nbetscore`, `nvalidbet`, `nresultmoney`, `nplayerscore`, `ntax`, `ngametype`, `nserverid`, `ncarddata`, `nbankid`, `szextchar`) VALUES ('17791002', '10428', '892885', '2', '10428-892885-1559843438-1', '1', '50000', '4', '2019-06-07 01:50:38.000', '2019-06-07 01:50:50.000', '73842', '1', '', '68349353', '50000', '50000', '-50000', '68299353', '0', '10', '1004', '2b3906', '0', '') /*percona-toolkit src_db:niuniu_db src_tbl:table_clubgamescoredetail src_dsn:h=192.168.1.10,p=...,u=pt_user dst_db:niuniu_db dst_tbl:table_clubgamescoredetail dst_dsn:h=192.168.1.11,p=...,u=pt_user lock:1 transaction:1 changing_src:consistency_db.checksums replicate:consistency_db.checksums bidirectional:0 pid:16713 user:coding001 host:db-b*/;


	[coding001@db-a ~]$ pt-table-sync --replicate=consistency_db.checksums h=192.168.1.10,u=pt_user,p=11 h=192.168.1.11,u=pt_user,p=11 --print
	REPLACE INTO `niuniu_db`.`table_clubgamescoredetail`(`id`, `nclubid`, `ntableid`, `nchairid`, `sztoken`, `nround`, `nbasescore`, `nplaycount`, `tstarttime`, `tendtime`, `nplayerid`, `brobot`, `szcarddata`, `nenterscore`, `nbetscore`, `nvalidbet`, `nresultmoney`, `nplayerscore`, `ntax`, `ngametype`, `nserverid`, `ncarddata`, `nbankid`, `szextchar`) VALUES ('17791002', '10428', '892885', '2', '10428-892885-1559843438-1', '1', '50000', '4', '2019-06-07 01:50:38.000', '2019-06-07 01:50:50.000', '73842', '1', '', '68349353', '50000', '50000', '-50000', '68299353', '0', '10', '1004', '2b3906', '0', '') /*percona-toolkit src_db:niuniu_db src_tbl:table_clubgamescoredetail src_dsn:h=192.168.1.10,p=...,u=pt_user dst_db:niuniu_db dst_tbl:table_clubgamescoredetail dst_dsn:h=192.168.1.11,p=...,u=pt_user lock:1 transaction:1 changing_src:consistency_db.checksums replicate:consistency_db.checksums bidirectional:0 pid:15167 user:coding001 host:db-a*/;


	 重复做 pt-table-checksum，会自动清空 checksums数据表的信息。
	"""