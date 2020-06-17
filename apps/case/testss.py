#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年06月17日00时50分44秒
from unittest import  util
import unittest
import sys
def strclass(cls):
    return "%s.%s" % (cls.__module__, cls.__qualname__)
class test_C():
    # def __init__(self,mothodName):
    #     self.mothodName=mothodName
    # # def __iter__(self):
    # #     return iter(self)
    # def __repr__(self):
    #     return "<%s testMethod=%s>" %(self.__class__,self.mothodName)
    # def __eq__(self, other):
    #     if type(self) is not type(other):
    #         return NotImplemented
    #
    #     return self.mothodName == other.mothodName
    # def __str__(self):
    #     return "%s (%s)" % (self.mothodName, self.__class__)
    def test_1(self):

        pass
    def test_2(self):
        pass
    def test_3(self):
        pass


class B(object):
    def __init__(self,tests=()):
        # self.b=1
        self.tests=[]
        self.add(tests)
    def __repr__(self):
        return "<%s tests=%s>"%(self.__class__,self.tests)
    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return list(self) == list(other)
    def __iter__(self):
        return iter(self.tests)

    def run(self,tests):
        for index, test in enumerate(self):
            return index,test
    def  add(self,tests):
        for a  in tests:
            self.tests.append(a)
class A(B):
    pass

if __name__=="__main__":
    a=test_C()
    l=[]
    print(a)
    print(a.__class__)
    def  is_callable(name):
        if name.startswith("test")  and  callable(getattr(a,name)):
            return getattr(a,name)
    f=list(filter(is_callable,dir(a)))
    l=[]
    for  name  in f:
        print(getattr(a,name))
        l.append(getattr(a,name))
    print(l)
    suite=A
    print(suite(l))







# A=TestSuite
# print(A)
# print(A([1,23,3,4,56]))



