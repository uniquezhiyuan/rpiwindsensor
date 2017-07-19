#!/bin/sh
#server chk
pid=$(pgrep -f server.py)
if [ -z $pid ];#empty is true
then
date "+%F %H:%M:%S" >>/var/log/wind.log
echo Process server.py unfortunately stopped ! Now restart server.py >>/var/log/wind.log
python3.6 /root/server.py
else
date "+%F %H:%M:%S" >>/var/log/wind.log
echo "Process server.py is running...">>/var/log/wind.log
fi

#server restart per 5 mins
pid=$(pgrep -f server.py)
kill -9 $pid
python3.6 /root/server.py
echo "Now server.py restarts." >>/var/log/wind.log
date "+%F %H:%M:%S" >>/var/log/wind.log
