#Pi wind check per min
pid=$(pgrep -f wind.py)
if [ -z $pid ];#empty is true
then
date "+%F %H:%M:%S" >>/var/log/wind.log
echo Process wind.py unfortunately stopped ! Now restart wind.py >>/var/log/wind.log
python3 /home/pi/wind/wind.py
else
date "+%F %H:%M:%S" >>/var/log/wind.log
echo "Process wind.py is running...">>/var/log/wind.log
fi

#Pi wind.py restart per min
pid=$(pgrep -f wind.py)
kill -9 $pid
python3 /home/pi/wind/wind.py
echo "Now wind.py restarts." >>/var/log/wind.log
date "+%F %H:%M:%S" >>/var/log/wind.log
