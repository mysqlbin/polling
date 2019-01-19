#!/usr/local/bin/python3
#coding=utf-8

import subprocess
import os
import shutil # 复制文件


cnf_file_path = '/etc/my_3306.cnf'
data_path = '/data/mysql/3306/'
tar_path = '/usr/local/mysql-5.7.24-linux-glibc2.12-x86_64.tar.gz'


# 1. 创建MySQL用户和用户组,并返回uid,gid

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


def get_uid_gid():
    cmd_getuid = 'id -u mysql'
    cmd_getgid = 'id -g mysql'
    # os.popen输出的结果并不是char类型，需要read()出来，并截取换行符
    uid = os.popen(cmd_getuid).read().strip('\n')
    gid = os.popen(cmd_getgid).read().strip('\n')
    #print('uid:', uid, 'gid:', gid)
    return (uid, gid)

# 2. 解压下载的二进制安装包
def untar(tar_path):
    try:
        #tar_path = tar_path
        #bin_path = '/usr/local/'
        # untar_cmd = 'tar -zxf {} -C {}'.format(tar_path, bin_path)
        untar_cmd = 'mkdir /usr/local/mysql && tar -xzvf {} -C /usr/local/mysql --strip-components 1'.format(tar_path)
        print(untar_cmd)
        (status, output) = subprocess.getstatusoutput(untar_cmd)
        if status == 0:
            print('untar finished')
        else:
            raise Exception
    except Exception:
        print('exec untar across a error')  # 如果程序走到这里，应该要结束掉

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
            print('chown mysql data dir success')
        else:
            raise Exception

    except OSError:
        print('create dir error,please check')
    return '/data/mysql/{}'


# 5. 初始化实例并读取临时密码
def initialize_instance(port):
    cmd = '/usr/local/mysql/bin/mysqld --defaults-file=/data/mysql/{}/my_3306.cnf --initialize'.format(port)
    (status, output) = subprocess.getstatusoutput(cmd)
    print('status:', status, 'detail:', output)
    if status == 0:
        print('Initialize finished,now read temporary password')


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


def main():

    add_mysql_user()
    untar(tar_path)
    base_dir_chown()
    tup = get_uid_gid()
    print (tup[0])
    print (tup[1])

    prepare(3306)

    cp_cnf(cnf_file_path, data_path)

    initialize_instance(3306)

if __name__ == '__main__':
    main()