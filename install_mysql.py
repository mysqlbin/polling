#!/usr/local/bin/python3
#coding=utf-8

import subprocess
import os
import shutil # 复制文件
from progressbar import *


#
# 设计用途：
#   基于二进制安装包，快速安装3306实例
# 基本用法：
#   上传 my_3306.cnf 文件到 /etc 目录下
#   上传MySQL的压缩包文件到 /usr/local 目录下


cnf_file_path = '/etc/my_3306.cnf'
data_path = '/data/mysql/3306/'
error_path = '/data/mysql/3306/data/error.log'
tar_path = '/usr/local/mysql-5.7.24-linux-glibc2.12-x86_64.tar.gz'


# 1. 创建MySQL用户和用户组

def add_mysql_user():
    try:
        cmd_create_group = 'groupadd mysql'
        (status, output) = subprocess.getstatusoutput(cmd_create_group)
        if status == 0:
            print('create group mysql success')
        else:
            raise Exception
        cmd_create_user = 'useradd -g mysql -d /usr/local/mysql -s /sbin/nologin -M mysql'
        (status, output) = subprocess.getstatusoutput(cmd_create_user)
        if status == 0:
            print('create user mysql success')
        else:
            raise Exception

    except Exception:
        print('create user and group mysql across a error,please check')

# 2. 返回 MySQL用户和用户组 的uid, gid
def get_uid_gid():
    cmd_getuid = 'id -u mysql'
    cmd_getgid = 'id -g mysql'
    # os.popen输出的结果并不是char类型，需要read()出来，并截取换行符
    uid = os.popen(cmd_getuid).read().strip('\n')
    gid = os.popen(cmd_getgid).read().strip('\n')
    print('uid:', uid, 'gid:', gid)
    # return (uid, gid)


# 2. 解压下载的二进制安装包
def untar(tar_path):
    try:
        #tar_path = tar_path
        #bin_path = '/usr/local/'
        # untar_cmd = 'tar -zxf {} -C {}'.format(tar_path, bin_path)
        untar_cmd = 'mkdir /usr/local/mysql && tar -xzvf {} -C /usr/local/mysql --strip-components 1'.format(tar_path)
        print ('start tar -xzvf mysql tar gz..........')
        pbar = ProgressBar().start()
        (status, output) = subprocess.getstatusoutput(untar_cmd)
        if status == 0:
            pbar.finish()
            print('untar finished')
        else:
            raise Exception
    except Exception:
        print('Exec untar across a error, Please check the zip file')
        exit()

# 3. 把mysql base dir 归属到mysql用户下
def base_dir_chown():
    try:
        mysql_base_dir = 'chown -R mysql:mysql /usr/local/mysql/'
        (status, output) = subprocess.getstatusoutput(mysql_base_dir)
        if status == 0:
            print('chown mysql base dir success')
        else:
            raise Exception
    except Exception:
         print('chown mysql base dir error')

# 4. 创建数据文件夹,并归属到mysql用户下

def prepare(port):
    try:
        os.makedirs('/data/mysql/{}/data'.format(port))
        os.mkdir('/data/mysql/{}/logs'.format(port))
        os.mkdir('/data/mysql/{}/tmp'.format(port))

        mysql_data_dir = 'chown -R mysql:mysql /data/mysql/{}/'.format(port)
        print (mysql_data_dir)
        (status, output) = subprocess.getstatusoutput(mysql_data_dir)
        if status == 0:
            print('mkdir data dir and chown mysql data dir success')
        else:
            raise Exception
    except OSError:
        print('create dir error,please check')


# 5. 初始化实例
def initialize_instance(port):

    pbar = ProgressBar().start()
    cmd = '/usr/local/mysql/bin/mysqld --defaults-file=/data/mysql/{}/my_3306.cnf --initialize'.format(port)
    (status, output) = subprocess.getstatusoutput(cmd)
    # print('status:', status, 'detail:', output)
    if status == 0:
        pbar.finish()
        print('Initialize finished,now read mysql login temporary password')

# 6. 接收指定的my.cnf文件，并复制到相关数据文件夹下
# TODO:自动询问关键参数，并生成my_$port.cnf

def cp_cnf(cnf_file_path, data_path):
    if os.path.exists(cnf_file_path):
        try:
            shutil.copy(cnf_file_path, data_path)
        except OSError:
            print('copy failed,please check it')
    else:
        print('file does`s not exist')

# 7. 提取错误日志中的密码
def get_error_password(error_path):

    # cat /data/mysql/3306/data/error.log |grep password
    cmd = 'cat {} |grep password'.format(error_path)
    (status, output) = subprocess.getstatusoutput(cmd)
    # print('status:', status, 'detail:', output)
    if status == 0:
        lists = output.split()
        print('\033[1;33;44m login method：\033[0m mysql -S /data/mysql/3306/data/3306.sock -p')
        print('\033[1;33;44m password: \033[0m %s' % (lists[-1]))


# 8. 启动数据库初始化
def start_mysql_init():
    #cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysql
    #/etc/init.d/mysql start OR /usr/local/mysql/bin/mysqld --defaults-file=/etc/my.cnf &(生成.sock文件)
    cmd = 'cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysql'
    (status, output) = subprocess.getstatusoutput(cmd)
    if status == 0:
        print('cp support-files/mysql.server to /etc/init.d/mysql success')


def start_mysql_server():
    #cmd = '/etc/init.d/mysql start'

    pbar = ProgressBar().start()
    cmd = '/usr/local/mysql/bin/mysqld --defaults-file=/data/mysql/3306/my_3306.cnf &'
    (status, output) = subprocess.getstatusoutput(cmd)
    if status == 0:
        pbar.finish()
        print('\033[1;33;44m mysql server start success \033[0m')
    else:
        print(output)
        
        #Starting MySQL.Logging to '/usr/local/mysql/data/mgr01.err'.
        #ERROR! The server quit without updating PID file (/usr/local/mysql/data/mgr01.pid).
        #说明 需要指定 my.cnf 配置文件

def main():

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("++                                          MySQL install start                                               ++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    add_mysql_user()
    untar(tar_path)
    base_dir_chown()
    prepare(3306)
    cp_cnf(cnf_file_path, data_path)
    initialize_instance(3306)
    get_error_password(error_path)
    start_mysql_init()
    start_mysql_server()

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("++                                          MySQL install sucesss                                             ++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

if __name__ == '__main__':
    main()