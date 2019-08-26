#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import MySQLdb

import smtplib
from email.mime.text import MIMEText

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
        sql = "update mysql.health_check set t_modified=now() where id=330601;"
        cursor.execute(sql)
        

    except Exception as e:
        print(e)
