#!/usr/local/bin/python3
#coding=utf-8
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


def main():

    tup = get_uid_gid()
    print (tup[0])
    print (tup[1])

    chown_child_file()

if __name__ == '__main__':

    main()