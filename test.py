#!/usr/local/bin/python3
#coding=utf-8

def get_uid_gid():
    uid = 'uid'
    gid = 'gid'
    return (uid,gid)

def main():

    tup = get_uid_gid()
    print (tup[0])
    print (tup[1])
if __name__ == '__main__':

    main()