#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年08月12日22时28分38秒
import pymysql,json
from libs.public import MyEncoder
from case.models import SqlStatement
from project.models import Environments

class Con_sql():
    """
    (
    0,链接数据库报错,
    1,结果处理成功
    2，执行sql失败
    3,结果处理失败
    )
    """
    def __init__(self,action=None,host=None,port=None,user=None,passwd=None,database=None,charset="utf8"):
        self.action=action   #sql结果处理方法，用户写的python脚本
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
        self.database=database
        self.charset=charset
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
            return {"code":1,"msg":"数据库连接成功"}
        except Exception as f:
            return {"code":0,"msg":"连接数据库报错:%s"%f}


    def runSql(self,sqlId,sql=None,status=None):
        res=self.connectSql()

        sqlObj = SqlStatement.objects.get(id=sqlId)
        method = self.action

        if not status:  #如果传了data则是说明使用前断传过来的参数进行处理
            sql=sqlObj.sql
            method = sqlObj.SqlActionResults
        if res["code"] :
            try:
                self.cursor.execute(sql)
                self.conn.commit()

                data=self.cursor.fetchall()
                self.cursor.close()
                if sqlObj.type==1:  #如果类型是查--则取出查的数据 做处理
                    if method:

                        value=self.SqlAction(method, data)
                        if value["strStatus"]==1:
                            self.envAction(sqlObj,value["res"])
                        else:
                            self.envAction(sqlObj, json.loads(value["res"]))
                        return value
                    else:
                        try:
                            value=json.dumps(data)
                            self.envAction(sqlObj, value)
                            return value
                        except Exception as f:
                            pass

                return {"code":1,"msg":"Sql执行成功","data":data}
            except pymysql.MySQLError as e:
                self.conn.rollback()
                return {"code":2,"msg":"SQL:%s操作失败，已完成回滚%s"%(sql,e)}
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
                a=eval(method)
                if type(a)==str:
                    resDict["res"]=a
                    resDict["strStatus"]=1
                else:
                    resDict["strStatus"] = 0
                    resDict["res"] =json.dumps(a)

            return resDict
        except Exception as e:
            resDict["code"]=3
            resDict["msg"]="sql执行结果处理错误:%s:"%e
            return resDict

    def envAction(self, data,value):
        """执行sql前置或者后置时处理环境变量
            需要优化--在更换保存的变量位置时  需要更换全局还是环境--在改变的时候---需要删除原来位置的变量--
        """
        key = data.name
        value = value
        saveResultChoice = json.loads(data.saveResultChoice)
        envId = data.envId.id
        if saveResultChoice:
            for item in saveResultChoice:
                if item == "保存到环境变量":
                    obj = Environments.objects.get(id=envId).value
                    obj=json.loads(obj)
                    objKeyList = list(map(lambda x: list(x.keys())[0], obj))
                    # obj[objKeyList.index(key)] = {key: value} if key in objKeyList else obj.append({key: value})
                    if key in objKeyList:
                        obj[objKeyList.index(key)] = {key: value}
                        Environments.objects.filter(id=envId).update(value=json.dumps(obj))
                    else:
                        obj.append({key: value})
                        Environments.objects.filter(id=envId).update(value=json.dumps(obj))

                if item == "保存到全局变量":
                    obj = Environments.objects.get(id=1).value
                    obj = json.loads(obj)
                    objKeyList = list(map(lambda x: list(x.keys())[0], obj))
                    # obj[objKeyList.index(key)] = {key: value} if key in objKeyList else obj.append({key: value})
                    if key in objKeyList:
                        obj[objKeyList.index(key)] = {key: value}
                        Environments.objects.filter(id=1).update(value=json.dumps(obj))
                    else:
                        obj.append({key: value})
                        Environments.objects.filter(id=1).update(value=json.dumps(obj))

                        # def
if __name__=="__main__":
    s=Con_sql(host="localhost",port=3306,user="root",passwd="123456",database="besettest")
    sql="SELECT * FROM `sql_box` where id=31"



    s=s.runSql(sql)["data"]
    print(s)
    a="c=s[0],type(c[1])"
    q=a.split(",")
    print(q)
    for  m in  q:
        exec(m)

    print(eval(q[-1]))