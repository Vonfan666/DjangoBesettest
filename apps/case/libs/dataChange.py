import  re
class dataChange(object):
    def __init__(self,headers,data):
        self.headers=headers
        self.data=data



    def run(self):
        self.replaceEnvironment(self.headers)
        self.replaceEnvironment(self.data)
        headers=self.headerChange()
        data=self.dataChange()
        return headers,data

    def headerChange(self):
        if self.headers == None or self.headers == "":
            return {}
        if len(self.headers["keys"])>0  and self.headers["keys"][-1]["headerKey"]=="":
            self.headers["keys"].pop()
        headersCode = {}
        for item in self.headers["keys"]:
            headersCode[item["headerKey"]] = item["headerValue"]
        return headersCode

    def dataChange(self):
        if self.data == None or self.data == "":
            return {}
        if len(self.data["keys"])>0  and self.data["keys"][-1]["dataKey"]=="":
            self.data["keys"].pop()
        dataCode={}
        for item in self.data["keys"]:
            dataCode[item["dataKey"]]=item["dataValue"]
        return dataCode

    def replaceEnvironment(self,data):
        re_s=re.compile(r"{{.+?}}")
        res=re_s.findall(data)
        if len(res)>0:
            for  item in res:
                #取出item的值去数据库里面查-查到之后--作为替换字符进去替换到花括号
                data=re_s.sub("headerValue",data,1)
            print(data)
            return data
true=True
headers={"keys":[{"headerKey":"{{Accept}}","headerValue":" application/json, text/plain, */*","headerDetail":"","key":1590475946741},{"headerKey":"Accept-Encoding","headerValue":" gzip, deflate","headerDetail":"","key":1590475946741},{"headerKey":"Accept-Language","headerValue":" zh-CN,zh;q=0.9","headerDetail":"","key":1590475946741},{"headerKey":"Authorization","headerValue":" JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNCwidXNlcm5hbWUiOiIxMzU5MDI4MzE4MiIsImV4cCI6MTU5MDk5NTg2MSwiZW1haWwiOiIifQ.pfkXSxxzyOMEreVJIxRlOtbaSadpPJTux1SWQNR7wUw","headerDetail":"","key":1590475946741},{"headerKey":"Connection","headerValue":" keep-alive","headerDetail":"","key":1590475946741},{"headerKey":"Cookie","headerValue":" csrftoken=W2qkPBcyrD4s7KReRKIiZNfsnLoLVv7TinPtRTiDQDIAOui2b3K3VEYyMeLGBvdF","headerDetail":"","key":1590475946741},{"headerKey":"Host","headerValue":" 192.168.0.66","headerDetail":"","key":1590475946741},{"headerKey":"Referer","headerValue":" http","headerDetail":"","key":1590475946741},{"headerKey":"User-Agent","headerValue":" Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36","headerDetail":"","key":1590475946741}]}
data={"keys":[{"isRequestsData":"true","dataKey":"","dataValue":"","dataDetail":""}]}
s=dataChange(headers,data)

print(s.run()[0])
print(s.run()[1])

