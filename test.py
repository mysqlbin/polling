# -*- coding: utf-8 -*-

import subprocess
import os

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


def main():

    #chown_child_file()

    row = '2019-01-19T07:38:14.928052Z 1 [Note] A temporary password is generated for root@localhost: 8l#)*gIbywER'
    lists = row.split()
    print lists   #type of list
    print lists[-1]


if __name__ == '__main__':

    main()