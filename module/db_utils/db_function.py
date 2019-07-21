
import pymysql
import argparse
import sys

def parse_args():
   parser = argparse.ArgumentParser()
   parser.add_argument('--host', type=str, default='192.168.1.27', help='Host the MySQL database server located')
   parser.add_argument('--user', type=str, default='root', help='MySQL Username to log in as')
   parser.add_argument('--password', default='123456abc', help='MySQL Password to use')
   parser.add_argument('--port', default=3306, type=int, help='MySQL port to use')
   return parser

def command_line_args(args):
    parser = parse_args()
    args = parser.parse_args(args)
    return args

def mysql_query(sql, user, passwd, host, port, get_data = 1):
    try:
        conn=pymysql.connect(host=host,user=user,passwd=passwd,port=int(port),connect_timeout=5,charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(sql)
        if get_data == 1:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as err:
        return err



def get_process_data(sql, get_data = 1):

    args = command_line_args(sys.argv[1:])
    user = args.user
    passwd = args.password
    host = args.host
    port = args.port

    results = mysql_query(sql, user, passwd, host, port, get_data)

    return results