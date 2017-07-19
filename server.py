import socket
from datetime import datetime
import time
import pymysql
addr=('45.127.97.71',6666)
#addr=('45.127.97.71',6666)
print('start server at {} '.format(datetime.now()))
print('waiting for client to connect...')
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(addr)
server.listen(1) #clients number
db=pymysql.connect('127.0.0.1','root','zhiyuan','wind')
print('MySQL connected!\r')
cursor=db.cursor()
def main():
    info1=client.recv(40).decode()
    info=info1[0:info1.find('\r')]
    speed=info[0:info.find(',')]
    position=info[info.find(',')+1:]
    cursor.execute('insert into windspeed values('+'\''+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\''+','+speed+','+'\"'+position+'\")')
    print(speed+','+position+'\n'+'Written!')

client,addr=server.accept()#pause to wait
print('connected!',datetime.now(),)
while 1:
    try:
        main()
    except:continue

