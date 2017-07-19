import serial
import pynmea2
import time
from math import e
from math import sqrt
from lcd import display

#GPS
def gpsget():
    ser0=serial.Serial('/dev/ttyUSB0',9600,timeout=1)
    try:byte=ser0.readline()
    except:pass
    try:str=byte.decode()
    except:pass
    if str.find('GPGGA')>0:
        msg=pynmea2.parse(str)
        return str
    else:return 'N/A'

def realtime():
    str=gpsget()
    realtime=str[7:9]+':'+str[9:11]+':'+str[11:13]
    return realtime

def latitude():
    str=gpsget()
    latitude=str[18:20]+'°'+str[20:22]+'.'+str[23:27]+'\''+'N'
    return latitude

def longitude():
    str=gpsget()
    longitude=str[30:33]+'°'+str[33:35]+'.'+str[36:40]+'\''+'E'
    return longitude

#GSM
#shortmessage='Bingo!'
def sendshortmessage(shortmessage):
    ser1=serial.Serial('/dev/ttyUSB1',115200,timeout=1)
    ser1.write(b'AT+CSCS="GSM"\r')
    time.sleep(1)
    ser1.write(b'AT+CMGF=1\r')
    time.sleep(1)
    ser1.write(b'AT+CMGS="15651783155"\r')
    time.sleep(1)
    ser1.write(bytes(shortmessage,encoding='utf8')+b'\r')
    time.sleep(1)
    ser1.write(b'\x1a\r')
    time.sleep(0)

#DATAGET
def portoperate():                              #端口操作
    ser2=serial.Serial('/dev/ttyUSB2',921600,timeout=1)            #初始化串口
    begin=bytes([170,9,2,161,0,0,187])          #定义开始指令，差分连续单通道模式
    stop=bytes([170,0,0,0,0,0,187])             #定义结束指令
    ser2.write(begin)                            #开始指令发送
    x=ser2.read(600)                             #数据接收，bytes类型
    ser2.write(stop)                             #结束采集
    ser2.write(stop)                             #结束采集
    ser2.close()                                 #关闭串口
    hexer=[hex(i) for i in bytes(x)]            #bytes转化为十六进制列表
    decer=[int(i,16) for i in hexer]            #转化为十进制列表
    voltage=[decer[i]//16*16**5+decer[i]%16*16**4+decer[i+1]//16*16**3+decer[i+1]%16*16**2+decer[i+2]//16*16**1+decer[i+2]%16*16**0 for i in range(0,600,3)]
                                                #转化为十进制电压数据
    return voltage                              #返回采集电压数据

def convert(n):                                 #转化为实际电压值
    if n//(16**5)<7:
        realvoltage=[n/16777215*10]
    else:
        realvoltage=[n/16777215-1]
    return realvoltage                          #返回实际电压值

def positive(n):                                #取绝对值
    if n>=0:positive=n*1.000000
    else:positive=-n*1.000000
    return positive                             #返回实际电压绝对值

def dataget():
    voltage=portoperate()                       #十进制电压数据
    realvoltage=[convert(voltage[i]) for i in range(0,200)]  #2D#200个电压真实值
    positive_realvoltage=[positive(realvoltage[i][0]) for i in range(0,200)]  #200个实际电压绝对值
    sum=0
    for i in range(0,200):
        sum+=positive_realvoltage[i]
    average=sum/200                             #200个采样数据均值
    return average

#DATAPROCESS
def fit1(x):
    return 0.00007525*x**2-0.0001306

def fit0(x):
    return 0.0003475*x-0.000003535

def windspeed1(y):
    return sqrt((y+0.0001306)/0.00007525)

def windspeed0(y):
    return sqrt((y+0.000003535)/0.0003475)

def windspeed(x):
    if x<0.0004:
        return windspeed0(x)-0.2
    else:
        return windspeed1(x)

# initialize GPRS module based on SIM900A
def gprsinitial():    
    ser1=serial.Serial('/dev/ttyUSB1',115200,timeout=1)
    ser1.write(b'AT+CGCLASS="B"\r')
    try:
        print(ser1.readline())
        print(ser1.readline())
    except:pass
    ser1.write(b'AT+CGDCONT=1,"IP","CMNET"\r')
    try:
        print(ser1.readline())
        print(ser1.readline())
    except:pass
    ser1.write(b'AT+CGATT=1\r')
    try:
        print(ser1.readline())
        print(ser1.readline())
    except:pass
    ser1.write(b'AT+CIPCSGP=1,"CMNET"\r')
    try:
        print(ser1.readline())
        print(ser1.readline())
    except:pass
    ser1.write(b'AT+CLPORT="TCP","2000"\r')
    try:
        print(ser1.readline())
        print(ser1.readline())
    except:pass
    ser1.write(b'AT+CIPSTART="TCP","45.127.97.71","6666"\r')
    try:
        print(ser1.readline())
        print(ser1.readline())
        print(ser1.readline())
        print(ser1.readline())
    except:pass

#create TCP connect to server with GPRS module
def tcpsend(info):
    ser1=serial.Serial('/dev/ttyUSB1',115200,timeout=1)
    ser1.write(b'AT+CIPSEND\r')
    ser1.write(bytes(info.encode())+b'\r') 
    ser1.write(b'\x1a\r')
    #ser1.write(b'AT+CIPSHUT\r')


global data_get #define a global variable
def speed():
        data_get=dataget()
        wind_speed='%.2f'%windspeed(data_get)
        if windspeed(data_get)>30:return speed()
        else:return wind_speed

#get GPS information with RPi GPS module
def position():
    try:
        position=latitude()+longitude()
    except:position='N/A'
    return position

def buffer():
    i=0 
    buffer=[]
    while 1:
        now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        buffer.append([now,str(windspeed()),str(position())])
        if len(buffer)>=20:
            return buffer
            break
        else:
            i+=1
            continue

def main():
    display('RealTimeSpeed:',str(speed())+'m/s')
    print('RealTimeSpeed:',str(speed())+'m/s'+'\r')
    try:info=speed()+','+position()
    except:info=speed()+','+'N/A'
    print('\r')
    tcpsend(info)
    print('\r')
    print(info+'\r'+'Sended!')
    print('\r')

while 1:
    try:
        gprsinitial()
        main()
    except:continue
