#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import MySQLdb

import smtplib
from email.mime.text import MIMEText
from common_utils.time_functions import  format_to_ymdx

def send_mail(body):

    host = 'smtp.163.com'
    port = 465
    sender = '13202095158@163.com'
    pwd = '20190809Go'
    receiver = ['13202095158@163.com', '1224056230@qq.com']
    body = body
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['subject'] = 'test'
    msg['from'] = sender
    msg['to'] = ",".join(receiver)

    try:
        s = smtplib.SMTP_SSL(host, port)
        s.login(sender, pwd)
        s.sendmail(sender, receiver, msg.as_string())
        print('Done.sent email success')
    except smtplib.SMTPException as e:
        print(e)
        print('Error.sent email fail')


if __name__ == '__main__':

    sql = 'select 1;'
    host = '192.168.0.54'
    user = 'root'
    passwd = '123456abc'
    port = 3306
    #
    # try:
    #     db = MySQLdb.connect(host, user, passwd, 'mysql', charset='utf8mb4')
    #     cursor = db.cursor()
    #     cursor.execute("select 1;")
    #     data = cursor.fetchone()
    #
    # except Exception as e:
    #     body = e
    #     send_mail(body)
    #     print(e)

    # sql = "update mysql.health_check set t_modified=now() where id=330601;"
    # cursor.execute(sql)
    # db.commit()

    try:
        db = MySQLdb.connect(host, user, passwd, 'mysql', charset='utf8mb4')
        cursor = db.cursor()


        t_modified = cursor.execute("select t_modified from mysql.health_check where id=330601;")

        data = cursor.fetchone()

        format_to_ymdx()

        sql = "update mysql.health_check set t_modified=now() where id=330601;"
        cursor.execute(sql)


    except Exception as e:
        body = e
        send_mail(body)
        print(e)
