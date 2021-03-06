#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年05月04日22时03分18秒

# -*- coding: utf-8 -*-
import socket,sys,io,time,json
from django_redis import get_redis_connection  as conn
from log.logFile import logger as logs


class Public():
    def get_host_ip(self):
        """获取ip地址"""
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(('8.8.8.8',8081))
            ip= s.getsockname()[0]
        finally:
            s.close()
        return ip

    def forData(self,data,res_data_c):
        """mock返回数据-将父子id的数据转换为标准的json数据
            type: [
                    {id:1,name: "string"},
                    {id:2,name: "number"},
                    {id:3,name: "boolean"},
                    {id:4,name: "object"},
                   {id:5,name: "array"},
                    {id:6,name: "file"},
                    {id:7,name: "null"},
                   ],
        """
        for item in data:
            if (item["type"] == "string" or item["type"] == 1 or item["type"] == 2 or item["type"] == 3 or item[
                "type"] == 6 or item["type"] == 7):
                # 如果当前对象是键值对-value是字符串则直接加进去-但是分上级是什么类型---
                if type(res_data_c) is dict:
                    res_data_c[item["cname"]] = item["mockValue"]
                if type(res_data_c) is list:
                    if item["type"]=="object" or item["type"]==4:
                        res_data_c.append({item["cname"]: item["mockValue"]})
                    else:#判断列表里面的是字符串还是-字典或者列表
                        res_data_c.append(item["cname"])
                    # if (item["type"]=="Array" or  item["type"]==5):
                    #     pass

                        # if len(res_data_c) > 0:
                        #     res_data_c[0][item["cname"]] = item["mockValue"]
                        # else:

            if (item["type"] == "object" or item["type"] == 4):
                # 如果当前对象是字典-判断上级对象是啥--
                if type(res_data_c) is dict:
                    # 如果上级对象是字典--则添加新的键值对 且value是一个字典
                    res_data_c[item["cname"]] = {}
                    # 继续遍历下级
                    self.forData(item["children"], res_data_c[item["cname"]])
                if (type(res_data_c) is list):
                    # 如果当前是字典-上级对象是list--则插入一个字典
                    res_data_c.append({item["cname"]: {}})
                    # 以下这句是找到当前插入字典的索引然后传给下一子递归
                    index = [(index, item1) for index, item1 in enumerate(res_data_c) if
                             list(item1.keys())[0] == item["cname"]][0][0]
                    # index=0
                    self.forData(item["children"], res_data_c[index][item["cname"]])
            if (item["type"] == "Array" or item["type"] == 5):
                if type(res_data_c) is dict:
                    res_data_c[item["cname"]] = []
                    if (len(item["children"]) > 0):
                        self.forData(item["children"], res_data_c[item["cname"]])
                if type(res_data_c) is list:
                    res_data_c.append({item["cname"]: []})
                    # 以下这句是找到当前插入字典的索引然后传给下一子递归
                    index = [(index, item1) for index, item1 in enumerate(res_data_c) if
                             list(item1.keys())[0] == item["cname"]][0][0]
                    # index=0
                    self.forData(item["children"], res_data_c[index][item["cname"]])
        return res_data_c

    def utcTime(self,code):
        if code:
            a = time.mktime(code.timetuple())
            code=time.strftime('%Y-%m-%d %X', time.localtime(a))
        return code


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self,fp,userId,interface,runTime):
        self.userId = userId
        self.interface = interface
        self.runTime = runTime
        self.start=sys.stdout
        self.logRedis = conn("log")
        self.fp = fp
    def write(self, s):
        self.fp.write(s)
        # key="%s_%s_%s"%(self.projectId,self.userId,self.runTime)
        self.logRedis.rpush("log:%s_%s"%(self.userId,self.interface), s)

        sys.stdout = self.start
    def writelines(self, lines):
        self.fp.writelines(lines)
    def flush(self):
        self.fp.flush()
class StartMethod(object):
    def __init__(self, userId=None, interface=None, runTime=None):
        self.userId = userId
        self.interface = interface
        self.runTime = runTime
        self.stdout_redirector = OutputRedirector(sys.stdout, self.userId, self.interface, self.runTime)
        self.stderr_redirector = OutputRedirector(sys.stderr, self.userId, self.interface, self.runTime)
        # self.startTest()
        # self.logger=logs(self.__class__.__module__)
    def __call__(self, *args, **kwargs):
        return self.startTest(*args, **kwargs)
    def startTest(self,*args, **kwargs):
        self.outputBuffer = io.StringIO()
        self.stdout_redirector.fp = self.outputBuffer
        self.stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout  # 记录标准输出原始位置
        self.stderr0 = sys.stderr
        sys.stdout = self.stdout_redirector
        sys.stderr = self.stderr_redirector



class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)
if __name__=="__main__":
    Publics=Public()