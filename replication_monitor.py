# -*- coding: utf-8 -*-
"""
__author__ = 
__date__ = 2018/09/29
"""
import sys
import pymysql
from dingtalkchatbot.chatbot import DingtalkChatbot
reload(sys)
sys.setdefaultencoding('utf-8')

webhook = 'https://oapi.dingtalk.com/robot/send?access_token=1f077306f882465984c4d9932afca61d6b85310093cda55bd14993a84f50446b'

xiaoding = DingtalkChatbot(webhook)

db_connect = pymysql.connect(
    host='192.168.1.11',
    user='',
    password='%',
    database='',
    port=3306,
    charset='utf8'
)

cur_write = db_connect.cursor()

def main():

    cur_write.execute("show slave status")

    res = cur_write.fetchone()

    if res:

        slave_io_running = res[10] # Slave_IO_Running

        slave_sql_running = res[11] # Slave_SQL_Running
        #print res[32]
        #为真时的结果 if 判定条件 else 为假时的结果
        seconds_behind_master = res[32] if res[32] is not None else 0 # Seconds_Behind_Master
        #print seconds_behind_master
        if  slave_io_running == 'No':
            xiaoding.send_markdown(
                title='rm封测从库监控',
                text=str('rm封测从库监控') + '\n'
                              '> IO Thread ' + slave_io_running + ' error\n',
                is_at_all=True
            )
        elif slave_sql_running == 'No':
            xiaoding.send_markdown(
                title='rm封测从库监控',
                text=str('rm封测从库监控') + '\n'
                              '> SQL Thread ' + slave_sql_running + ' error\n',
                is_at_all=True
            )
        elif seconds_behind_master != 0:
            xiaoding.send_markdown(
                title='rm封测从库监控',
                text=str('rm封测从库监控') + '\n'
                              '> 延迟 ' + str(seconds_behind_master),
                is_at_all=True
            )
        else:
            print ''


if __name__ == '__main__':

    main()
