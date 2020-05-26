import  re,json
from libs.errors import errorsMsg
class dataChange(object):
    def __init__(self,headers,data,environment=None):
        self.headers=headers
        self.data=data
        self.environment=environment
        self.headers = self.headerChange()
        self.data = self.dataChange()

    def run(self):
        """执行方法"""
        self.isDataType(self.headers,self.data)
        headers=self.replaceEnvironment(self.headers)
        data=self.replaceEnvironment(self.data)
        print(headers,data)
        print(type(headers),type(data))
        return json.loads(headers),json.loads(data)

    def headerChange(self):
        """处理请求头格式"""
        if self.headers == None or self.headers == "":
            return {}
        if len(self.headers["keys"])>=0  and self.headers["keys"][-1]["headerKey"]=="":
            self.headers["keys"].pop()
        print(self.headers)
        headersCode = {}
        for item in self.headers["keys"]:
            headersCode[item["headerKey"].strip()] = item["headerValue"].strip()
        return headersCode

    def dataChange(self):
        """处理请求数据格式"""
        if self.data == None or self.data == "":
            return {}
        if len(self.data["keys"])>=0  and self.data["keys"][-1]["dataKey"]=="":
            self.data["keys"].pop()
        dataCode={}
        for item in self.data["keys"]:
            dataCode[item["dataKey"].strip()]=item["dataValue"].strip()
        return dataCode

    def replaceEnvironment(self,data):
        """将用户填写的环境变量替换成具体字符串"""
        print(data)
        re_s=re.compile(r"{{.+?}}")
        res=re_s.findall(data)
        print(res)
        if len(res)>0:
            for  item in res:
                item=self.itemDataRe(item)
                print(item)
                #取出item的值去数据库里面查-查到之后--作为替换字符进去替换到花括号
                data=re_s.sub(item,data,1)
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
        re_s = re.compile(r"{{(.+?)}}")
        res = re_s.findall(item)
        print(type(self.environment))
        print(self.environment)
        envi=self.environment["environment"][0]
        glob = self.environment["global"][0]
        if res[0] in envi.keys():
            value = envi[res[0]]
            return value
        elif res[0] in glob.keys():
            value = glob[res[0]]
            return value
        else:
            errorsMsg["Message"]="%s变量不存在"%(res[0])
            raise Exception("%s变量不存在啊"%(res[0]))




# true=True
# headers={"keys":[{"headerKey":"{{Accept}}","headerValue":" application/json, text/plain, */*","headerDetail":"","key":1590475946741},{"headerKey":"Accept-Encoding","headerValue":" gzip, deflate","headerDetail":"","key":1590475946741},{"headerKey":"Accept-Language","headerValue":" zh-CN,zh;q=0.9","headerDetail":"","key":1590475946741},{"headerKey":"Authorization","headerValue":" JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNCwidXNlcm5hbWUiOiIxMzU5MDI4MzE4MiIsImV4cCI6MTU5MDk5NTg2MSwiZW1haWwiOiIifQ.pfkXSxxzyOMEreVJIxRlOtbaSadpPJTux1SWQNR7wUw","headerDetail":"","key":1590475946741},{"headerKey":"Connection","headerValue":" keep-alive","headerDetail":"","key":1590475946741},{"headerKey":"Cookie","headerValue":" csrftoken=W2qkPBcyrD4s7KReRKIiZNfsnLoLVv7TinPtRTiDQDIAOui2b3K3VEYyMeLGBvdF","headerDetail":"","key":1590475946741},{"headerKey":"Host","headerValue":" 192.168.0.66","headerDetail":"","key":1590475946741},{"headerKey":"Referer","headerValue":" http","headerDetail":"","key":1590475946741},{"headerKey":"User-Agent","headerValue":" Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36","headerDetail":"","key":1590475946741}]}
# data={"keys":[{"isRequestsData":"true","dataKey":"","dataValue":"","dataDetail":""}]}
# s=dataChange(headers,data)
#
# print(s.run()[0])
# print(s.run()[1])
