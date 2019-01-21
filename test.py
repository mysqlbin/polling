# -*- coding: utf-8 -*-

import subprocess
import os

import time
from progressbar import *


def get_uid_gid():
    uid = 'uid'
    gid = 'gid'
    return (uid,gid)


def chown_child_file():
   #chown -R mysql:mysql /usr/local/mysql/
   mysql_base_dir = 'chown -R mysql:mysql /usr/local/mysql/'
   (status, output) = subprocess.getstatusoutput(mysql_base_dir)
   if status == 0:
       print('chown success')
   else:
       raise Exception

def split_log_get_password():
    row = '2019-01-19T07:38:14.928052Z 1 [Note] A temporary password is generated for root@localhost: 8l#)*gIbywER'
    text_list = row.split()



def dosomework():
    time.sleep(0.01)

def pp():
    p = ProgressBar()
    N = 1000
    p.start(N)
    for i in range(N):
        time.sleep(0.01)
        p.update(i + 1)
    p.finish()

def pp2():
    total = 1000

    def dosomework():
        time.sleep(0.01)

    progress = ProgressBar()
    for i in progress(range(100)):
        dosomework()

def untar():
    try:

        # p = ProgressBar()

        tar_path = '/usr/local/mysql-5.7.24-linux-glibc2.12-x86_64.tar.gz'

        untar_cmd = 'mkdir /usr/local/mysqls && tar -xzvf {} -C /usr/local/mysqls --strip-components 1'.format(tar_path)
        # print(untar_cmd)
        print ('start tar -xzvf mysql tar gz..........')
        pbar = ProgressBar().start()

        (status, output) = subprocess.getstatusoutput(untar_cmd)

        pbar.finish()

        if status == 0:
            print('untar finished')
        else:
            raise Exception
    except Exception as e:

        print(e)
        exit()

def input():
    num = 7
    num1 = input("x: ")

    if num1 == num:
        print("猜对了")
    else:
        print("猜错了")

def main():

    #chown_child_file()

    # row = '2019-01-19T07:38:14.928052Z 1 [Note] A temporary password is generated for root@localhost: 8l#)*gIbywER'
    # lists = row.split()
    # print lists   #type of list
    # print lists[-1]

    # progress = ProgressBar()
    # for i in progress(range(1000)):
    #     dosomework()

    #pp2()
    #pp()
    # untar()

    age = int(input("请输入你家狗狗的年龄: "))
    print("")
    if age < 0:
        print("你是在逗我吧!")
    elif age == 1:
        print("相当于 14 岁的人。")
    elif age == 2:
        print("相当于 22 岁的人。")
    elif age > 2:
        human = 22 + (age - 2) * 5
        print("对应人类年龄: ", human)

    ### 退出提示
    input("点击 enter 键退出")

if __name__ == '__main__':

    main()