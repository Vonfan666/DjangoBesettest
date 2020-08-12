#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年08月12日22时28分38秒
import pymysql
class Con_sql():
    def __init__(self,action=None,host=None,port=None,user=None,passwd=None,database=None,charset="utf8"):
        self.action=action
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
        self.database=database
        self.charset=charset
    def __call__(self, *args, **kwargs):
        return self.runSql(*args)
    def connectSql(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.passwd,
                database=self.database,
                charset=self.charset
            )
            self.cursor = self.conn.cursor()
            return {"code":1,"msg":""}
        except Exception as f:
            return {"code":0,"msg":"连接数据库报错:%s"%f}


    def runSql(self,sql):
        res=self.connectSql()

        if res["code"]:
            try:
                self.cursor.execute(sql)
                self.conn.commit()

                data=self.cursor.fetchall()
                self.cursor.close()
                value=self.SqlAction(self.action, data)
                return value
            except Exception as e:
                self.conn.rollback()
                return {"code":0,"msg":"数据处理失败，已完成回滚%s"%e}
        else:

            return res

    def SqlAction(self,method,data):
        resDict={
            "code":1,
            "msg":"",
            "data":data,
            "res":None
        }
        res = data
        try:
            if  "," in method:
                methodList=method.split(",")
                for item  in  methodList:
                    exec(item)
                resDict["res"]=eval(methodList[-1])
                return resDict
            else:

                resDict["res"] = eval(method)
            return resDict
        except Exception as e:
            resDict["code"]=0
            resDict["msg"]="sql执行结果处理错误:%s:"%e
            return resDict

    # def
if __name__=="__main__":
    s=Con_sql(host="localhost",port=3306,user="root",passwd="123456",database="besettest")
    s=s("SELECT * FROM `sql_box` where id=32;")
    print(s)
    a="c=s[0],c[1]"
    q=a.split(",")
    print(q)
    for  m in  q:
        exec(m)

    print(eval(q[-1]))