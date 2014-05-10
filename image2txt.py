# -*- coding:utf-8 -*-
#!/usr/bin/env python
#filename:image2text.py
#author:longming_xu

"""
    本程序实现了功能：将图片转化为字符形式的txt文件
"""

import os, sys
#ini操作模块（内置）
import ConfigParser
#判断图片格式模块（内置）
import imghdr

try:
    #图片处理模块PIL(非内置)
    import Image
except ImportError, e:
    print "ERROR:you have not install PIL Library [PIL-1.1.7.win32-py2.7.exe]!", e
    sys.exit(1)

#全局
CURRENTPATH = os.getcwd()
CHARS = "   ...',;:clodxkO0KXNWMMMM"

#后缀：暂时支持这几种
STUFFIXS = ['.jpg', '.jpeg', '.tiff', '.png', 'bmp']

def getNewSize(image):
    """
        将原图片大小按比例缩放
    """
    t_width = image.size[0]
    t_height = image.size[1]

    n_width = 100
    #按比例缩放
    #n_width(100) = 缩放系数 * t_width
    #n_height = 缩放系数 * t_height
    #
    n_height = n_width * t_height / t_width
    
    return int(n_width), int(n_height)


def image2Text(t_filesrc, t_filedest):
    """
        功能：主题函数实现图片到文本的转换，主要是根据灰度图256色来处理
        参数：
            t_filesrc : 要处理的图片文件绝对路径
            t_filedest ：要保存的对应文本文件绝对路径
    """
    output = ""
    try:
        image = Image.open(t_filesrc)
    except IOError, e:
        print u"ERROR:this file is not pic or open error!", e
        return 0
    else:
        #根据原图片大小得到一个新size,因为转化原理：是将像素放大表现出来了，这里的放大是指用文本表示像素点（所以考虑分辨率问题，将图片缩放）
        newsize = getNewSize(image)
        #重新设置大小（比例缩放）
        image = image.resize(newsize)
        #转化为256级灰度图
        image = image.convert("L")
        #获取图片像素信息
        pixs = image.load()

        print u"图片大小:(%s,%s);像素信息：%d" %(image.size[0], image.size[1], image.size[0] * image.size[1]) 

        #遍历每行像素（图片中实际像素值范围0-255）
        for y in range(newsize[1]):
            for x in range(newsize[0]):
                #10为基准，共26个色段（0-25）
                output += CHARS[pixs[x, y] / 10]
            #一行结束
            output += '\n'

        #写入文件中
        f = open(t_filedest, "w")
        f.write(output)
        f.close()
        return 1
 
    
def getConfigInfo():
    """
        功能：读取config.ini文件中的路径信息
        picsrc:图片源文件夹
        picdest:转换后文本的保存文件夹
    """
    global CURRENTPATH
    
    cp = ConfigParser.ConfigParser()
    try:
        cf = open(os.path.join(CURRENTPATH, "config.ini"))
    except IOError, e:
        print e
        sys.exit(1)
    else:
        cp.readfp(cf)
        cf.close()

    try:
        picsrc = cp.get("PATH", "picsrc")
        picdest = cp.get("PATH", "picdest")
    except ConfigParser.NoSectionError, e:
        print e
        sys.exit(1)
    except ConfigParser.NoOptionError, e:
        print e
        sys.exit(1)

    #如果配置文件路径设为""，则默认在当前路径创建文件夹
    if picsrc == "":
        picsrc = os.path.join(CURRENTPATH, "picsrc")
    if picdest == "":
        picdest = os.path.join(CURRENTPATH, "picdest")

    if not os.path.exists(picsrc):
        print "ERROR:%s is not exist! program will create it!" %picsrc
        os.makedirs(picsrc)
        sys.exit(1)

    if not os.path.exists(picdest):
        os.makedirs(picdest)  

    return picsrc, picdest

def IsImage(flag, filePath):
    """
        功能：判断一个文件是否是图片格式
        flag="suffix" 判断后缀
        flag="header"判断文件头标识(建议：因为后缀名可以随便修改)
    """
    if flag == "stuffix":
        filename = os.path.split(filePath)[1]
        #判断名文件后缀是否在STUFFIXS中
        for stuffix in STUFFIXS:
            if filename.endswith(stuffix):
                return True
        return False
    
    elif flag == "header":
        #使用内置模块：该模块实现比较简单主要是读取文件头标记
        if imghdr.what(filePath) != None:
            return True
        else:
            return False
    
    
def main():
    """
        功能：入口函数
    """
    #获取config.ini文件中的配置信息
    srcpath, destpath = getConfigInfo()

    #获取目录下的（图片）文件（注意：只能放图片）
    fileList = os.listdir(srcpath)

    if len(fileList) <= 0:
        print "WARING:%s  is empty!" % srcpath
        sys.exit(1)

    #遍历每个（图片）文件
    for simpleFileName in fileList:
        #这里可以加上判断文件是不是图片(一种判断文件后缀flag="suffix"；一种判断文件头标识flag="header")
        #flag = IsImage("suffix", os.path.join(srcpath, simpleFileName))
        flag = IsImage("header", os.path.join(srcpath, simpleFileName))
        
        #如果是图片则执行下面转换
        if flag == True:
            #转换后的文本文件名字
            newTextFileName = "%s_%s.txt" %(simpleFileName.split(".")[0], simpleFileName.split(".")[1])

            print simpleFileName, "---->>>>>>>>", newTextFileName

            #这里才是重点：把图片转换成文本文件
            result = image2Text(os.path.join(srcpath, simpleFileName), os.path.join(destpath, newTextFileName))

            if result == 1:
                print u"-------->>>>>>>success\n"
            else:
                print u"-------->>>>>>>failed\n"
        else:
            print simpleFileName, u"警告：不是图片或不支持该图片格式\n"

if __name__ == "__main__":
    main()
    raw_input(u"enter to quit!")

