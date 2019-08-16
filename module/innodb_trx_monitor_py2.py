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
cur_write.execute("select trx_id, trx_state, trx_started, trx_mysql_thread_id, trx_query  from information_schema.innodb_trx where TIME_TO_SEC(timediff(now(),trx_started)) > 60;")
res = cur_write.fetchone()

if res:

    trx_id              = res[0]
    trx_state           = res[1]
    trx_started         = res[2]
    trx_mysql_thread_id = res[3]
    trx_query           = res[4]

    body = '<h1>长事务信息如下:</h1> \
           <p>trx_id:%s </p> \
           <p>trx_state:%s </p> \
           <p>trx_started:%s </p> \
           <p>trx_mysql_thread_id:%s </p> \
           <p>trx_query:%s </p> ' % \
             (trx_id, trx_state, trx_started, trx_mysql_thread_id, trx_query)

    #body = 'Seconds_Behind_Master: %s' % seconds_behind_master

    msg = MIMEText(body, 'html', 'utf-8')
    msg['subject'] = 'Problem: 2rm db1 long uncommitted transactions'
    msg['from'] = sender
    msg['to'] = ",".join(receiver)

    try:
        s = smtplib.SMTP_SSL(host, port)
        s.login(sender, pwd)
        s.sendmail(sender, receiver, msg.as_string())
        print('Done.sent email success')

    except smtplib.SMTPException:
        print('Error.sent email fail')
