#!/usr/local/bin/python3
#coding=utf-8
import subprocess

# (命令正常执行返回0，报错则返回1)
def IO_scheduler():
    x=input('输入yes进行IO调度算法的优化：')
    command = '''echo 'deadline' >/sys/block/sda/queue/scheduler'''
    if x == 'yes':
        print('now do:', command)
        (status, output)=subprocess.getstatusoutput(command)
        if status == 0:
            print ("\033[1;33;46m IO scheduling changed\033[0m")
        if status != 0:
            print('\033[1;32;41m fail,please check manually \033[0m!')


def open_files():
    x = input('输入yes优化文件打开数量：')
    command1 = '''echo '* soft nofile 65536' >>/etc/security/limits.conf'''
    command2 = '''echo '* hard nofile 65536' >>/etc/security/limits.conf'''
    if x == 'yes':
        print('now do:', command1)
        (status, output)=subprocess.getstatusoutput(command1)
        if status == 0:
            print ("\033[1;33;46m open files changed online\033[0m")
        if status != 0:
            print('\033[1;32;41m fail,please check manually \033[0m!')
        print('now do:', command2)
        (status, output)=subprocess.getstatusoutput(command2)
        if status == 0:
            print ("\033[1;33;46m open files changed online\033[0m")
        if status != 0:
            print('\033[1;32;41m fail,please check manually \033[0m!')

def disable_numa():
    x = input('输入yes关闭NUMA(需联网)：')
    command1 = '''yum -y install numactl'''
    command2 = '''numactl --interleave=all'''
    if x == 'yes':
        print('now do:', command1)
        (status, output)=subprocess.getstatusoutput(command1)
        if status == 0:
            print ("\033[1;33;46m numactl is installed successfully\033[0m")
        if status != 0:
            #print('fail,please check manually')
            print('\033[1;32;41m error please check manually \033[0m!')
    if x == 'yes':
        print('now do:', command2)
        (status, output)=subprocess.getstatusoutput(command2)
        if status == 0:
            print ("\033[1;33;46m NUMA close successfully\033[0m")
        if status != 0:
            print('\033[1;32;41m please restart system,check again \033[0m!')

def suggest(cmd, title, suggest):
    (status,output) = subprocess.getstatusoutput(cmd)
    print ('''
----------------------------------------------------------------------------------------------------------------
    ''')
    print("######{}#######".format(title))
    print(output)
    print("*******{}*******".format(suggest))

suggest("df -Th|awk '{print $1,$2}'|grep -v 'tmpfs'","1.查看文件系统","建议data分区为xfs")
suggest("cat /sys/block/sda/queue/scheduler","2.查看IO调度算法","建议采用deadline算法，不要用cfg算法")
IO_scheduler()
suggest("ulimit -a|grep 'open files'","3.查看文件打开数","建议设置为系统最大65535")
open_files()
suggest("grep -i numa /var/log/dmesg","4.NUMA是否开启","强烈建议关闭NUMA")
disable_numa()
# suggest("sysctl -a | grep swappiness","5.swap占用比","建议值设置为1-10")
# suggest("sysctl -a | grep dirty_ratio","6.dirty刷新脏页比1","设置为10比较好")
# suggest("sysctl -a | grep dirty_background_ratio","7.dirty刷新脏页比2","设置为5比较好")


