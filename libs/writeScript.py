#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年06月05日00时30分34秒

import  re,os,json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class MakeScript(object):
    def __init__(self):
        self.classSample=open("{}/interface/CaseScriptSample/classSample.py".format(BASE_DIR),"r",encoding="utf8")
        self.importSample=open("{}/interface/CaseScriptSample/importSample.py".format(BASE_DIR),"r",encoding="utf8")
        self.methodSample=open("{}/interface/CaseScriptSample/methodSample.py".format(BASE_DIR),"r",encoding="utf8")
        # self.file=open("{}/interface/test_all.py".format(BASE_DIR),"a",encoding='utf8')

        self.classSampleText=self.classSample.readlines()
        self.importSampleText = self.importSample.readlines()
        self.methodSampleText = self.methodSample.readlines()
    def write(self, s):
        pass

    def make_replace_class(self,classNameC,order):

        for text  in self.classSampleText:
             if "class_name_code"  in   text:   #进行类名替换

                 text=text.replace("class_name_code","TestCase_{}".format(order.zfill(7)))
             if  "__class_name__"  in text:
                 text =text.replace("__class_name__",classNameC)  #替换unittest获取的类名
             self.makeFile.write(text)
    def make_replace_import(self):
        for text  in  self.importSampleText:
            self.makeFile.write(text)

    def make_replace_method(self,row):
        for text in self.methodSampleText:
            if "__method_name__" in text:
                text =text.replace("__method_name__",row["name"])
            if "test_method_name" in text:
                text =text.replace("test_method_name","test_{}".format(str(row["order"]).zfill(7)))
            if "data={}" in text:
                text=text.replace("data={}","data=%s"%(row))
            self.makeFile.write(text)
        #以下是数据库存的断言数据[{post:1,res:2},{}]  断言post与res的区别--如果列表存在多个则遍历添加断言
        #前端填写断言格式为res["xxx"]
        self.makeFile.write("        self.assertEqual({}, {})\n".format(200,"res['status']"))

        #写入断言--数据库直接存 assertEqual(a, b)  这种格式
    def writelines(self, lines):
        pass

    def make_close(self):
        self.makeFile.close()
        self.classSample.close()
        self.methodSample.close()
        self.importSample.close()

    def start_write(self):
        pass
    def order_data(self,data):
        return  sorted(data,key=lambda data:data["order"])
    def make_file(self,data,name):
        """执行函数"""

        self.makeFile=open("{}/interface/testFiles/{}.py".format(BASE_DIR,name),"a",encoding="utf8")
        #添加import
        self.make_replace_import()
        for item in data:
            if len(item["child"])>0:
                #创建一个class
                self.make_replace_class(item["name"],str(item["order"]))
                #如果该接口下存在用例--则第一步是给该接口下的所有用例排序
                interfaceCaseList=self.order_data(item["child"])
                for  row in  interfaceCaseList:
                    #创建用例def
                    self.make_replace_method(row)



            else:
                pass
                #如果只有文件没有内容的---考虑是否处理-后面再说
        self.makeFile.flush()
        self.make_close()
if __name__=="__main__":
    files=MakeScript()




