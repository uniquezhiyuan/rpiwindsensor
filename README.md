# rpiwindsensor
Raspberry Pi based wind speed sensor.
Used a Raspberry Pi, a USB data collecting board, a USB GPS module,a serial port SIM900A module, a LCD1602 module to make a wind speed sensor. This divice is a kind of solid wind sensor and can test wind speed all the time.

detail here:
https://zhuanlan.zhihu.com/p/31640250

树莓派实现的固态测风装置，涉及Python串口编程读取数据采集卡电压数据，Python数据库编程保存风速数据，树莓派LCD1602模块显示数据，GPS模块Python解析天线的NMEA编码经纬度和时间数据，SIM900模块串口编程建立TCP连接上传数据至Linux服务器中的MySQL数据库，Shell编程监控服务器端（VPS）和客户端（树莓派）程序运行状态适时重启并记录日志，Web前端实时风速变化曲线可视化动态显示。

详细介绍：
https://zhuanlan.zhihu.com/p/31640250
