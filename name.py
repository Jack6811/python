import xlrd
import random
import tkinter as tk
import pygame
import time
import os

#打开网络文件
#name = ("https://raw.githubusercontent.com/Jack6811/python/master/name.xls")
#s = request.urlopen(name).read().decode('xls')
#dfile = StringIO(s)
#creader = csv.reader(dfile) 
#dlists=[rw for rw in creader] 

#创建文件夹
# 去除首位空格
#path=path.strip()
# 去除尾部 \ 符号
#path=path.rstrip("\\")
 
# 判断路径是否存在
# 存在     True
# 不存在   False
isExists=os.path.exists("log")
 
# 判断结果
if not isExists:
    # 如果不存在则创建目录
        # 创建目录操作函数
    os.makedirs("log") 
 
        
#        return True
#    else:
#        # 如果目录存在则不创建，并提示目录已存在
#        print path+' 目录已存在'
#        return False

#时间设定
time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

#ini配置
ini = open('config.ini',mode='w')
ini.writelines(['[common]\n'])
ini.writelines(['#随机方式：name为名字随机，number为学号随机\n'])
ini.writelines(['way = name\n'])
ini.writelines(['#性别对待：all为不区别，bay为男生，girl为女生\n'])
ini.writelines(['gender = all\n'])
# 创建管理对象
#conf = configparser.ConfigParser()
# 读ini文件
#conf.read(cfgpath, encoding="utf-8")  # python3
# 获取所有的section
#ections = conf.sections()
#print(sections)  # 返回list
#items = conf.items('email_163')
#print(items)  # list里面对象是元祖

#基础设定
workbook = xlrd.open_workbook("name.xls")  # 读取表格
Data_sheet = workbook.sheets()[0]  # 读取sheet1
name_list = Data_sheet.col_values(0)  # 读取第A列
data = set()  # 一个空set保存选过的同学

#更新日志
gengxin = open('更新日志.txt',mode='w+')
gengxin.writelines(['更新日志 1.2.6  2019年11月19日\n','1.修复字体差异，统一为宋体\n','2.将开始键调大，方便点击\n','3.添加更新日志\n','\n','\n'])
gengxin.writelines(['更新日志 1.3.4  2019年11月23日\n','1.更改图标\n','\n','\n'])
gengxin.writelines(['更新日志 1.3.7  2019年12月5日\n','1.添加日志功能\n','\n','\n'])
gengxin.close()

root = tk.Tk()
root.title("随机点名  by:苏畅  1.3.7")
#URL可视化图标
#root.iconbitmap('./beta/2019.ico')
root.geometry('500x150')
 
global var
var = tk.StringVar()
on_strat = False
 
l = tk.Label(root, textvariable=var, font=('simsun', 35), width=20, height=2)
l.pack()
 
def start():
    try:
        rdata = random.choice(name_list)
        if on_strat==False:
            name_list.remove(rdata)
            #print("["+time+"]"+" "+rdata) 打印日志
            #os.mknod('.//log//'+ time + ".log")
            log = open("运行日志.log",mode='a')
            log.writelines("["+time+"]"+":"+" "+rdata+"\n")
            if rdata not in data:
                    var.set(rdata)
                    data.add(rdata)
        if len(name_list)==0:
            var.set("所有同学已经点过")
            log = open("运行日志.log",mode='a')
            log.writelines(["\n","\n","\n","\n","\n","\n","\n"])
    except ValueError as e:
        var.set("所有同学已经点过")
B = tk.Button(root, font=('simsun', 25), width=6, height=1, text="开始", command=start)
B.pack()
 

root.mainloop()
