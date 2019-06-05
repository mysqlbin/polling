#!/bin/bash
# T-Bone Lu
#
trap 'cleanup' SIGUSR1 SIGINT SIGHUP SIGQUIT SIGTERM SIGSTOP
PROGRAMNAME=${0##*/}
VERSION=1.2

logDir=/var/log
logfile=synctime.log

cleanup() {
        exit 0
}

echo "Original Hardware Clock:" | tee -a ${logDir}/${logfile}
hwclock | tee -a ${logDir}/${logfile}

echo "Original System Clock:" | tee -a ${logDir}/${logfile}
date | tee -a ${logDir}/${logfile}


echo "Fix Timezone : Asia/Shanghai -> localtime"  | tee -a ${logDir}/${logfile}
ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime | tee -a ${logDir}/${logfile}

echo "Synchronize Time :""$textc_s" | tee -a ${logDir}/${logfile} 
ntpdate time4.google.com | tee -a ${logDir}/${logfile}

echo "Correction System Clock:" |tee -a ${logDir}/${logfile}
date | tee -a ${logDir}/${logfile}

echo "Set the Hardware Clock to the current System Time!" |tee -a ${logDir}/${logfile}
clock -w | tee -a ${logDir}/${logfile}

echo "Correction Hardware Clock:" | tee -a ${logDir}/${logfile}
hwclock | tee -a ${logDir}/${logfile}
echo | tee -a ${logDir}/${logfile}





#显示硬件时钟
hwclock
[root@mgr9 ~]# hwclock
Fri 26 Apr 2019 04:49:38 PM CST  -0.432877 seconds


#修改时区
echo "Fix Timezone : Asia/Shanghai -> localtime"  | tee -a /var/log/synctime.log
ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime | tee -a ${logDir}/${logfile}
tee -a tee -a /var/log/synctime.log    #把 "Fix Timezone : Asia/Shanghai -> localtime"写入/var/log/synctime.log 文件


#[root@database-05 ~]# clock
Fri 26 Apr 2019 04:57:04 PM CST  -0.100801 seconds



#ntpdate  时间同步
ntpdate time4.google.com

tee -a 输入的日志信息:
Original Hardware Clock:
Original System Clock:
Sun Apr 21 00:00:01 CST 2019
Fix Timezone : Asia/Shanghai -> localtime
Synchronize Time :
Correction System Clock:
Sun Apr 21 00:00:01 CST 2019
Set the Hardware Clock to the current System Time!
Correction Hardware Clock:


Google（谷歌）提供的NTP服务，以下4个域名
http://time1.google.com
http://time2.google.com
http://time3.google.com
http://time4.google.com
