from django.test import TestCase

# Create your tests here.
data= \
    [{"cname": "status", "isrequired": "ture", "type": "string", "detail": "", "id": 1, "parentId": 0, "children": [],
      "mockValue": "傻逼"},
     {"cname": "msg", "isrequired": "ture", "type": "string", "detail": "", "id": 2, "parentId": 0, "children": [],
      "mockValue": "1"},
     {"cname": "result", "isrequired": "ture", "type": "object", "detail": "", "id": 3, "parentId": 0, "children": [
         {"cname": "pageEnity", "isrequired": "ture", "type": "object", "detail": "", "id": 4, "parentId": 3,
          "children": [
              {"cname": "currentPage", "isrequired": "ture", "type": "string", "detail": "", "id": 5, "parentId": 4,
               "children": [], "mockValue": "1"},
              {"cname": "pageSize", "isrequired": "ture", "type": "string", "detail": "", "id": 6, "parentId": 4,
               "children": [], "mockValue": "1"},
              {"cname": "totalCount", "isrequired": "ture", "type": "string", "detail": "", "id": 7, "parentId": 4,
               "children": [], "mockValue": "1"},
              {"cname": "totalPage", "isrequired": "ture", "type": "string", "detail": "", "id": 8, "parentId": 4,
               "children": [], "mockValue": "1"}], "mockValue": ""},
         {"cname": "list", "isrequired": "ture", "type": "Array", "detail": "", "id": 9, "parentId": 3, "children": [
             {"cname": "imageUrl", "isrequired": "ture", "type": "string", "detail": "", "id": 10, "parentId": 9,
              "children": [], "mockValue": "1"},
             {"cname": "desc", "isrequired": "ture", "type": "string", "detail": "", "id": 11, "parentId": 9,
              "children": [], "mockValue": "1"}], "mockValue": ""}], "mockValue": ""},
     {"cname": "cao", "isrequired": "ture", "type": "string", "detail": "", "id": 12, "parentId": 0, "children": [],
      "mockValue": "傻逼"},
     {"cname": "312312", "isrequired": "true", "type": 5, "detail": "", "id": 14, "parentId": 0, "mockValue": "",
      "children": [
          {"cname": "第二个", "isrequired": "true", "type": 4, "detail": "", "id": 17, "parentId": 14, "mockValue": "",
           "children": [
               {"cname": "2", "isrequired": "true", "type": 1, "detail": "", "id": 19, "parentId": 17, "mockValue": "1",
                "children": []},
               {"cname": "1", "isrequired": "true", "type": 1, "detail": "", "id": 18, "parentId": 17, "mockValue": "1",
                "children": []}]},
          {"cname": "31231", "isrequired": "true", "type": 4, "detail": "", "id": 15, "parentId": 14, "mockValue": "",
           "children": [{"cname": "haha ", "isrequired": "true", "type": 1, "detail": "", "id": 16, "parentId": 15,
                         "mockValue": "1", "children": []},
                        {"cname": "32131", "isrequired": "true", "type": 1, "detail": "", "id": 16, "parentId": 15,
                         "mockValue": "1", "children": []}]}]},
     {"cname": "空dict", "isrequired": "true", "type": 4, "detail": "", "id": 20, "parentId": 0, "mockValue": "",
      "children": []}]
res_data_c1={}
def forData(data, res_data_c):
    for item in data:
        print(res_data_c)
        if (item["type"] == "string" or item["type"]==1 or item["type"]==2 or item["type"]==3 or item["type"]==6 or item["type"]==7 ):
            #如果当前对象是键值对-value是字符串则直接加进去-但是分上级是什么类型---
            if type(res_data_c) is dict:
                res_data_c[item["cname"]] = item["mockValue"]
            if type(res_data_c) is list:
                res_data_c.append({item["cname"]:item["mockValue"]})
        if (item["type"] == "object" or item["type"]==4):
            #如果当前对象是字典-判断上级对象是啥--
            if type(res_data_c) is dict:
                #如果上级对象是字典--则添加新的键值对 且value是一个字典
                res_data_c[item["cname"]] = {}
                #继续遍历下级
                forData(item["children"], res_data_c[item["cname"]])
            if(type(res_data_c) is list):
                # 如果当前是字典-上级对象是list--则插入一个字典
                    res_data_c.append({item["cname"]: {}})
                    print(res_data_c1)
                #以下这句是找到当前插入字典的索引然后传给下一子递归
                    index=[ (index,item1) for  index,item1  in  enumerate(res_data_c) if list(item1.keys())[0]==item["cname"]][0][0]
                    print(index)
                    forData(item["children"], res_data_c[index][item["cname"]])
        if (item["type"] == "Array" or item["type"]==5):
            res_data_c[item["cname"]] = []
            if(len(item["children"])>0):
                forData(item["children"], res_data_c[item["cname"]])
    return  res_data_c

print(forData(data,res_data_c1))
