#!/usr/local/bin/python3
#coding=utf-8

from db_utils.db_function import get_process_data


def get_param_value(param = ''):
    sql = "show global variables like '{:s}'".format(param)
    results = get_process_data(sql)
    if results:
        res = '{} : {}'.format(results[0], results[1])
        print(res)

def get_status_value(param = '',only_get_val = 1):
    sql = "show global status like '{:s}'".format(param)
    results = get_process_data(sql)
    if results:
        if only_get_val == 1:
            res = '{} : {}'.format(results[0], results[1])
            print(res)
        else:
            res = results[1]
            return res
