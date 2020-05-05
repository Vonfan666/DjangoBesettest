#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年05月04日22时03分18秒

# -*- coding: utf-8 -*-
import socket
class Public():
    def get_host_ip(self):
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
            print(res_data_c)
            if (item["type"] == "string" or item["type"] == 1 or item["type"] == 2 or item["type"] == 3 or item[
                "type"] == 6 or item["type"] == 7):
                # 如果当前对象是键值对-value是字符串则直接加进去-但是分上级是什么类型---
                if type(res_data_c) is dict:
                    res_data_c[item["cname"]] = item["mockValue"]
                if type(res_data_c) is list:
                    res_data_c.append({item["cname"]: item["mockValue"]})
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
                    print(res_data_c)
                    # 以下这句是找到当前插入字典的索引然后传给下一子递归
                    index = [(index, item1) for index, item1 in enumerate(res_data_c) if
                             list(item1.keys())[0] == item["cname"]][0][0]
                    print(index)
                    self.forData(item["children"], res_data_c[index][item["cname"]])
            if (item["type"] == "Array" or item["type"] == 5):
                res_data_c[item["cname"]] = []
                if (len(item["children"]) > 0):
                    self.forData(item["children"], res_data_c[item["cname"]])
        return res_data_c
if __name__=="__main__":
    Publics=Public()