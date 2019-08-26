#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import psutil
reload(sys)

import smtplib
from email.mime.text import MIMEText

# CPU利用信息
def get_cpu_info(verbose):
    cpu_info = {}
    # if verbose > 0:
    #     print "[cpu]    start collect cpu info ..."
    data = psutil.cpu_times_percent()
    cpu_info['user'] = data[0]        # 用户空间使用
    cpu_info['system'] = data[2]      # 内核空间使用
    cpu_info['idle'] = data[3]        # 空闲
    cpu_info['iowait'] = data[4]      # io等待
    cpu_info['hardirq'] = data[5]     # 硬中断
    cpu_info['softirq'] = data[6]     # 软中断
    cpu_info['cpu_cores'] = psutil.cpu_count()    #CPU核数
    # if verbose > 0:
    #     print "[cpu]    collection compeleted ..."
    return cpu_info

#内存利用信息
def get_mem_info(verbose):
    mem_info = {}
    # if verbose > 0:
    #     print("[mem]    start collect mem info ...")
    data = psutil.virtual_memory()
    mem_info['total'] = round(data[0]/1024/1024/1024,4)      #总内存大小
    mem_info['avariable'] = round(data[1]/1024/1024/1024,4)  #可利用内存大小
    # if verbose > 0:
    #     print("[mem]  collection compeletd ...")
    return mem_info

#磁盘利用信息
def get_disk_info(verbose):
    disk_info={}
    # if verbose > 0:
    #     print "[disk]    start collect disk info ..."
    partitions = psutil.disk_partitions()
    partitions = [(partition[1],partition[2]) for partition in partitions if partition[2]!='iso9660']
    for partition in partitions:
        disk_info[partition[0]] = {}
        disk_info[partition[0]]['fstype'] = partition[1]            #文件系统类型
    for mount_point in disk_info.keys():
        data = psutil.disk_usage(mount_point)
        disk_info[mount_point]['total'] = round(data[0]/1024/1024/1024, 4)    #磁盘空间大小
        disk_info[mount_point]['used_percent'] = data[3]                     #占用磁盘空间的比例
    # if verbose > 0:
    #     print"[disk]    collection compeleted ...."
    return disk_info

def send_mail(body, format = 'plain'):

    host = 'smtp.163.com'
    port = 465
    sender = '13202095158@163.com'
    pwd = '20190809Go'
    receiver = ['13202095158@163.com', '1224056230@qq.com']
    body = body
    msg = MIMEText(body, format, 'utf-8')
    msg['subject'] = 'Info: 2rm db1 操作系统层监控'
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

    cpu_info = get_cpu_info(1)
    # print cpu_info
    #
    mem_info = get_mem_info(1)
    # print mem_info
    #
    disk_info = get_disk_info(1)
    # print disk_info
    
    body = 'cpu: %s, memory: %s, disk: %s' %  (cpu_info, mem_info, disk_info)

    send_mail(body)

