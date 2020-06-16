#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年06月17日00时50分44秒
from unittest import  util
class BaseTestSuite(object):
    def __init__(self,a):
        self.a=a
        self.b=1
        self.tests=[]
    def __repr__(self):

        return "<%s tests=%s>"%(util.strclass(self.__class__),self.tests)
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return list(self) == list(other)
    def __iter__(self):
        return iter(self.tests)

    def  cc(self):
        return self
    def bb(self):
        return 1


print(BaseTestSuite(1).cc())
class TestSuite(BaseTestSuite):
    pass