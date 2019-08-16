#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import MySQLdb
reload(sys)

import smtplib
from email.mime.text import MIMEText

host = 'smtp.163.com'
port = 465
sender = ''
pwd = ''
receiver = []

sys.setdefaultencoding('utf-8')
db_connect = MySQLdb.connect(
    host='',
    user='',
    passwd='',
    db='',
    port=3306,
    charset='utf8mb4'
)

cur_write = db_connect.cursor()
cur_write.execute("show slave status")
res = cur_write.fetchone()

if res:

    slave_io_running = res[10]  # Slave_IO_Running
    slave_sql_running = res[11]  # Slave_SQL_Running

    if not res[32]:
        seconds_behind_master = None
    elif res[32] > 0:
        seconds_behind_master = res[32]
    else:
        seconds_behind_master = 0

    if slave_io_running == 'No':
        body = 'Slave_IO_Running: No'
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['subject'] = 'Problem: 2rm db2 Slave_IO_Running error'
        msg['from'] = sender
        msg['to'] = ",".join(receiver)
        try:
            s = smtplib.SMTP_SSL(host, port)
            s.login(sender, pwd)
            s.sendmail(sender, receiver, msg.as_string())
            print('Done.sent email success')

        except smtplib.SMTPException:
            print('Error.sent email fail')
    elif slave_sql_running == 'No':
        body = 'Slave_IO_Running: No'
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['subject'] = 'Problem: 2rm db2 Slave_IO_Running error'
        msg['from'] = sender
        msg['to'] = ",".join(receiver)
        try:
            s = smtplib.SMTP_SSL(host, port)
            s.login(sender, pwd)
            s.sendmail(sender, receiver, msg.as_string())
            print('Done.sent email success')

        except smtplib.SMTPException:
            print('Error.sent email fail')

    elif seconds_behind_master > 10:

        body = 'Seconds_Behind_Master: %s' % seconds_behind_master

        msg = MIMEText(body, 'plain', 'utf-8')
        msg['subject'] = 'Problem: 2rm db2 Seconds_Behind_Master has delay'
        msg['from'] = sender
        msg['to'] = ",".join(receiver)
        try:
            s = smtplib.SMTP_SSL(host, port)
            s.login(sender, pwd)
            s.sendmail(sender, receiver, msg.as_string())
            print('Done.sent email success')

        except smtplib.SMTPException:
            print('Error.sent email fail')

    else:
        print 'no error'