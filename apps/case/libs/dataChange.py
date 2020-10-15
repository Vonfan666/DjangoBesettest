import  re,json
from libs.errors import errorsMsg
import  logging
# logger =  logging.getLogger("log")

class dataChange(object):
    def __init__(self,headers,data,logger,url,environment=None):
        self.headers=headers
        self.data=data
        self.logger=logger
        self.environment=environment
        self.headers = self.headerChange()
        self.data = self.dataChange()
        self.url=url

    def run(self):
        """执行方法"""

        self.isDataType(self.headers,self.data)
        headers=self.replaceEnvironment(self.headers)
        data=self.replaceEnvironment(self.data)
        url=self.replaceEnvironment(self.url)

        return json.loads(headers),json.loads(data),url

    def headerChange(self):
        """处理请求头格式"""
        if self.headers == None or self.headers == "":
            return {}
        if type(self.headers)==str:
            try:
                self.headers=json.loads(self.headers)
            except:
                errorsMsg["Message"] = "请求头数据非JSON数据"
                return {}

        if len(self.headers["keys"])>0  and self.headers["keys"][-1]["headerKey"]=="":
            self.headers["keys"].pop()
        headersCode = {}
        for item in self.headers["keys"]:
            headersCode[item["headerKey"].strip()] = item["headerValue"].strip()
        return headersCode



    def dataChange(self):
        """处理请求数据格式"""
        if self.data == None or self.data == "" :
            return {}
        if type(self.data)==str:
            try:
                self.data=json.loads(self.data)
            except:
                errorsMsg["Message"] = "请求数据非JSON数据"
                return {}

        if len(self.data["keys"])>0  and self.data["keys"][-1]["dataKey"]=="":
            self.data["keys"].pop()
        dataCode={}
        for item in self.data["keys"]:
            dataCode[item["dataKey"].strip()]=item["dataValue"].strip()
        return dataCode

    def replaceEnvironment(self,data):

        """将用户填写的环境变量替换成具体字符串"""
        re_s=re.compile(r"{{.+?}}")
        res=re_s.findall(data)
        if len(res)>0:
            for  item in res:
                value=self.itemDataRe(item)
                #取出item的值去数据库里面查-查到之后--作为替换字符进去替换到花括号
                if type(value)==str:  #如果是字符串则直接替换
                    data=re_s.sub(value,data,1)
                if type(value)==int:  #如果item是整数则需要另外的替换方式
                    data=json.loads(data)    #从所有的data列表里面找出当前的item进行替换
                    dataList=list(data.values())
                    dataKeyList=list(data.keys())
                    if len(dataList)>0:
                        for index,row  in enumerate(dataList):
                            if row==item:

                                data[dataKeyList[index]]=value
                    data=json.dumps(data)

        else:
            data=data
        return data

    def isDataType(self,headers,data):
        """判断是否为字符串，不是字符串则转成json数据"""
        if not isinstance(headers,str):
            self.headers=json.dumps(headers)
        if not isinstance(data,str):
            self.data=json.dumps(data)

    def itemDataRe(self,item):
        """匹配环境变量"""
        re_s = re.compile(r"{{(.+?)}}")
        res = re_s.findall(item)

        envi=self.environment["environment"] if len(self.environment["environment"])>0 else False
        value=None
        if envi:
            enviKeysList=list(map(lambda x:list(x.keys())[0],envi))
            if res[0] in enviKeysList:
                enviIndex=enviKeysList.index(res[0])
                value = envi[enviIndex][res[0]]
        if not value:#如果在环境变量没找到则取全局变量找
            value=self.globalDataRe(res)
        if not value: #如果全局变量没找到-则抛出异常
            errorsMsg["Message"] = "%s变量不存在" % (res[0])
            data=json.dumps({"header":json.loads(self.headers),"data":json.loads(self.data),"url":self.url,"msg":"%s变量不存在"%(res[0])})
            raise Exception(data)

        return value

    def globalDataRe(self,res ):
        value=None
        glob = self.environment["global"] if len(self.environment["global"]) > 0 else False
        if glob:
            globKeysList = list(map(lambda x: list(x.keys())[0], glob))
            if res[0] in globKeysList:
                globIndex = globKeysList.index(res[0])
                value = glob[globIndex][res[0]]

        return value




# true=True
# headers={"keys":[{"headerKey":"{{Accept}}","headerValue":" application/json, text/plain, */*","headerDetail":"","key":1590475946741},{"headerKey":"Accept-Encoding","headerValue":" gzip, deflate","headerDetail":"","key":1590475946741},{"headerKey":"Accept-Language","headerValue":" zh-CN,zh;q=0.9","headerDetail":"","key":1590475946741},{"headerKey":"Authorization","headerValue":" JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNCwidXNlcm5hbWUiOiIxMzU5MDI4MzE4MiIsImV4cCI6MTU5MDk5NTg2MSwiZW1haWwiOiIifQ.pfkXSxxzyOMEreVJIxRlOtbaSadpPJTux1SWQNR7wUw","headerDetail":"","key":1590475946741},{"headerKey":"Connection","headerValue":" keep-alive","headerDetail":"","key":1590475946741},{"headerKey":"Cookie","headerValue":" csrftoken=W2qkPBcyrD4s7KReRKIiZNfsnLoLVv7TinPtRTiDQDIAOui2b3K3VEYyMeLGBvdF","headerDetail":"","key":1590475946741},{"headerKey":"Host","headerValue":" 192.168.0.66","headerDetail":"","key":1590475946741},{"headerKey":"Referer","headerValue":" http","headerDetail":"","key":1590475946741},{"headerKey":"User-Agent","headerValue":" Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36","headerDetail":"","key":1590475946741}]}
# data={"keys":[{"isRequestsData":"true","dataKey":"","dataValue":"","dataDetail":""}]}
# s=dataChange(headers,data)
#
# print(s.run()[0])
# print(s.run()[1])

