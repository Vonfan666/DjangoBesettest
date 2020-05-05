#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年05月04日01时03分54秒

class Validated_data():
    def  __init__(self,validated_data,initial_data):
        self.validated_data=validated_data
        self.initial_data=initial_data
        # self.models=models
    def validated_data_add(self, validated_data,models, postKey, updateKey):

        if postKey not in self.validated_data.keys() and self.initial_data[postKey]!= "":
            value = self.initial_data[postKey]
            obj = models.objects.get(id=value)
            validated_data[updateKey] = obj
            return validated_data
