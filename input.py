#!/usr/local/bin/python3
#coding=utf-8

import subprocess

version_dict = {
    'mysql-5_7_20': 'https://dev.mysql.com/Downloads/MySQL-5.7/mysql-5.7.20-linux-glibc2.12-x86_64.tar.gz',
    'mysql-5_7_21': 'https://dev.mysql.com/Downloads/MySQL-5.7/mysql-5.7.21-linux-glibc2.12-x86_64.tar.gz',
    'mysql-5_7_22': 'https://dev.mysql.com/Downloads/MySQL-5.7/mysql-5.7.22-linux-glibc2.12-x86_64.tar.gz',
    'mysql-5_7_23': 'https://dev.mysql.com/Downloads/MySQL-5.7/mysql-5.7.23-linux-glibc2.12-x86_64.tar.gz',
    'mysql-5_7_24': 'https://dev.mysql.com/Downloads/MySQL-5.7/mysql-5.7.24-linux-glibc2.12-x86_64.tar.gz',
}


def input_go():

    print('''
You have 5 options for you Database version install.
1: Install MySQL 5.7.20
2: Install MySQL 5.7.21
3: Install MySQL 5.7.22
4: Install MySQL 5.7.23
5: Install MySQL 5.7.24
    ''')

    version = int(input("Enter your choice (1, 2, 3, 4, 5): "))  #这里再加一个 y/n
    if version == 1:
        version = 'mysql-5_7_20'
    elif version == 2:
        version = 'mysql-5_7_21'
    elif version == 3:
        version = 'mysql-5_7_22'
    elif version == 4:
        version = 'mysql-5_7_23'
    elif version == 5:
        version = 'mysql-5_7_24'
    else:
        version = 'mysql-5_7_24'
    return version
    ### 退出提示
    #input("点击 enter 键退出")


def main():
    try:
        version_addr = input_go()
        print(version_dict[version_addr])
        download_mysql_cmd = 'wget -P {} {}'.format('/usr/local/',version_dict[version_addr])
        (status, output) = subprocess.getstatusoutput(download_mysql_cmd)
        if status == 0:
            print(output)
            print('wget mysql finished')
        else:
            print(output)
            raise Exception
    except Exception:
        print('wget mysql error, Please check the http addr')
        exit()
    print(1111)
if __name__ == '__main__':

    main()