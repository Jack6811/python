import xlrd
import random
import tkinter as tk
import pygame
from time import strftime
import os
import win32com.client as win
import sys

#朗读
speak = win.Dispatch("SAPI.SpVoice")

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
 
#生成资源文件目录访问路径,即封装外部调用文件，见https://blog.csdn.net/weixin_34037977/article/details/86017938
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

#基础设定
workbook = xlrd.open_workbook("name.xls")  # 读取表格
Data_sheet = workbook.sheets()[0]  # 读取sheet1
name_list = Data_sheet.col_values(0)  # 读取第A列
data = set()  # 一个空set保存选过的同学

#更新日志
gengxin = open('更新日志.txt',mode='w+')
gengxin.writelines(['更新日志 1.2.6  2019年11月19日\n','   1.修复字体差异，统一为宋体\n','   2.将开始键调大，方便点击\n','   3.添加更新日志\n','\n','\n'])
gengxin.writelines(['更新日志 1.3.4  2019年11月23日\n','1.更改图标\n','\n','\n'])
gengxin.writelines(['更新日志 1.3.7  2019年12月5日\n','1.添加日志功能\n','\n','\n'])
gengxin.writelines(['更新日志 1.3.10  2020年9月19日\n','   1.添加语音提示\n','   2.修复日志时间戳\n','   3.修复了日志功能\n', '   4.修正了窗口大小，使其可以进行全屏适配\n', '   5.更新了图标\n','   6.修复了一些已知bug\n''\n','\n'])
gengxin.close()

#创建日志
desktop_path = os.getcwd() + "\\log\\"  # 新创建的txt文件的存放路径
full_path = desktop_path + "运行日志" + strftime('[%Y-%m-%d %H-%M-%S]') + '.log' # 也可以创建一个.doc的word文档
logger = open(full_path, 'a')
logger.writelines(["\n","\n","\n","\n","\n","\n","\n"])
          
root = tk.Tk()
root.title("随机点名 V1.3.10")
#URL可视化图标
ico = resource_path('icon/die.ico') #导入图标
root.iconbitmap(ico)
root.geometry('640x480')
 
global var
var = tk.StringVar()
on_strat = False
 
l = tk.Label(root, textvariable=var, font=('simsun', 40), width=25, height=8)
l.pack()

def start():
    try:
        rdata = random.choice(name_list)
        if on_strat==False:
            name_list.remove(rdata)
            print(strftime('[%Y-%m-%d %H:%M:%S]') +" "+rdata) #打印日志
            #时间设定
            logger = open(full_path, 'a')
            logger.writelines(strftime('[%Y-%m-%d %H:%M:%S]') +":"+" "+rdata+"\n")
            speak.Speak(rdata)
            if rdata not in data:
                    var.set(rdata)
                    data.add(rdata)
        if len(name_list)==0:
            var.set("所有同学已经点过")
            speak.Speak("所有同学已经点过")
    except ValueError as e:
        var.set("所有同学已经点过")
        speak.Speak("所有同学已经点过")
B = tk.Button(root, font=('simsun', 30), width=10, height=1, text="开始", command=start)
B.pack()

root.mainloop()
speak.Speak(start)
