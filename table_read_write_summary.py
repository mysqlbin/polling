#!/usr/bin/env python
#-*- coding:utf-8 -*-

import MySQLdb
import time
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''
DROP TABLE IF EXISTS `table_read_write_day_list`;
create table table_read_write_day_list(
	`ID` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
	`database_name` varchar(15)  not null DEFAULT '' COMMENT '数据库名',
	`filename` varchar(50)  not null DEFAULT '' COMMENT '文件名',
	`table_name` varchar(50)  not null DEFAULT '' COMMENT '表名',
	`count_read` int(11) NOT NULL COMMENT '总共有多少次读',
	`count_write` int(11) NOT NULL COMMENT '总共有多少次写',
	`date_time` varchar(12) not null comment '统计时间-年月日',
	`execute_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '统计时间',
	PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据库表的读写每天统计表';

DROP TABLE IF EXISTS `table_read_write_day_summary`;
create table table_read_write_day_summary(
	`ID` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
	`database_name` varchar(15)  not null DEFAULT '' COMMENT '数据库名',
	`table_name` varchar(50)  not null DEFAULT '' COMMENT '表名',
	`count_read_day` int(11) NOT NULL COMMENT '昨天到今天有多少次读',
	`count_read_all` int(11) NOT NULL COMMENT '截止到现在总共有多少次读',
	`count_write_day` int(11) NOT NULL COMMENT '昨天到今天有多少次写',
	`count_write_all` int(11) NOT NULL COMMENT '截止到现在总共有多少次写',
	`date_time` varchar(12) not null comment '统计时间-年月日',
	`execute_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '统计时间',
	PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据库表的计算每天读写表';

truncate table_read_write_day_list;
truncate table_read_write_day_summary;

INSERT INTO table_read_write_day_list(database_name, filename, table_name, count_read, count_write, date_time) VALUES("niuniuh5_db", "table_web_loginlog.ibd", "table_web_loginlog", 333432, 63201, "2019-05-13");
INSERT INTO table_read_write_day_list(database_name, filename, table_name, count_read, count_write, date_time) VALUES("niuniuh5_db", "table_web_loginlog11.ibd", "table_web_loginlog", 333432, 63201, "2019-05-14")


思路：
    1. 遍历今天得到的数据去跟昨天的数据做比较；
    2. 做统计插入

'''

date_y_m_d = time.strftime("%Y-%m-%d")

database_name = 'niuniuh5_db'

conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='', db=database_name, charset='utf8', unix_socket="/data_volume/mysql/mysql.sock")
# conn = MySQLdb.connect(host='', port=3306, user='root', passwd='', db=database_name, charset='utf8')
cursor = conn.cursor()

cursor.execute(
    "select file, count_read, count_write from sys.io_global_by_file_by_bytes where file like '@@datadir/niuniuh5_db%' and (count_read > 500 or count_write > 500);")
list_info = cursor.fetchall()
if list_info:
    for lists in list_info:
        file_name = lists[0].replace('@@datadir/niuniuh5_db/', '')
        table_name = lists[0].replace('@@datadir/niuniuh5_db/', '')[:-4]
        count_read = lists[1]
        count_write = lists[2]
        try:
            insert_sql = 'INSERT INTO table_read_write_day_list(database_name, filename, table_name, count_read, count_write, date_time) VALUES("%s", "%s", "%s", %s, %s, "%s")' % (
                database_name, file_name, table_name, count_read, count_write, date_y_m_d)
            print insert_sql
            cursor.execute(insert_sql)
            conn.commit()
        except Exception as e:
            print e
            conn.rollback()
            break

time.sleep(1)

# 取今天得到的数据， 写入table_read_write_day_summary
cursor.execute(
    "select table_name, sum(count_read), sum(count_write) from table_read_write_day_list where date_time='%s' group by table_name" % (
        time.strftime("%Y-%m-%d")))
day_info = cursor.fetchall()
if day_info:
    for info in day_info:
        table_name = info[0]
        count_read = info[1]
        count_write = info[2]
        try:

            insert_sql = 'INSERT INTO table_read_write_day_summary(database_name, table_name, count_read_day, count_read_all, count_write_day, count_write_all, date_time) VALUES("%s", "%s", %s, %s, %s, %s, "%s")' \
                  % (database_name, table_name, 0, count_read, 0, count_write, date_y_m_d)
            print insert_sql
            cursor.execute(insert_sql)
            conn.commit()
        except Exception as e:
            print e
            conn.rollback()
            break

time.sleep(1)

#从table_read_write_day_summary取今天得到的数据去跟昨天的做比较
cursor.execute("select table_name, sum(count_read_all), sum(count_write_all) from table_read_write_day_summary where date_time='%s' group by table_name" % (time.strftime("%Y-%m-%d")))
summary_info = cursor.fetchall()
if summary_info:
    for summary in summary_info:
        table_name = summary[0]
        count_read_all = summary[1]
        count_write_all = summary[2]
        #去取昨天的数据
        cursor.execute(
            "select sum(count_read), sum(count_write) from table_read_write_day_list where date_time='%s' and table_name='%s'" % (
                datetime.date.today() + datetime.timedelta(-1), table_name))
        result = cursor.fetchone()
        if result[0] != None:

            '''
            print result
            print result[0]
            print result[1]
            print count_read_all
            print count_write_all
            '''
            day_count_read = count_read_all -  result[0]
            day_count_write = count_write_all -  result[1]
            '''
            print day_count_read
            print day_count_write
            '''

            udpate_sql = "update table_read_write_day_summary set count_read_day = %s, count_write_day = %s, execute_time='%s' where table_name='%s' and date_time= '%s'" \
                         % (day_count_read, day_count_write, time.strftime("%Y-%m-%d %H:%M:%S"), table_name,
                            time.strftime("%Y-%m-%d"))
            print udpate_sql
            cursor.execute(udpate_sql)
            conn.commit()

        '''
        try:
            if before_res:
                udpate_sql = "update table_read_write_day_summary set count_read_day = %s, count_write_day = %s, execute_time='%s' where table_name='%s' and date_time= '%s'"\
                             % (count_read, count_write, time.strftime("%Y-%m-%d %H:%M:%S"), table_name, time.strftime("%Y-%m-%d"))
                print udpate_sql
                cursor.execute(udpate_sql)
                conn.commit()
        except Exception as e:
            print e
            conn.rollback()
            break
        '''


