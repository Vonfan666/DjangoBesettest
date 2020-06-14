#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年05月04日01时03分54秒

class Validated_data():
    # def  __init__(self,validated_data,initial_data):
    #     self.validated_data=validated_data
    #     self.initial_data=initial_data
    #     # self.models=models
    def validated_data_add(self, validated_data,initial_data,models, postKey, updateKey):

        print(postKey  in validated_data.keys())

        if postKey not in validated_data.keys() and  postKey in initial_data.keys()  :
            if initial_data[postKey]!= "":
                value = initial_data[postKey]
                obj = models.objects.get(id=value)
                validated_data[updateKey] = obj
