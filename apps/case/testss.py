#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年06月17日00时50分44秒
from unittest import  util
import unittest
import sys
class TestResult(object):
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        self.failfast = False
        self.failures = []
        self.errors = []
        self.testsRun = 0
        self.skipped = []
        self.expectedFailures = []
        self.unexpectedSuccesses = []
        self.shouldStop = False
        self.buffer = False
        self.tb_locals = False
        self._stdout_buffer = None
        self._stderr_buffer = None
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._mirrorOutput = False


class TestCase(object):
    def __init__(self,name):
        self.name=name
        name = getattr(self, name)
        self.run()

    def __repr__(self):
        return "<%s testMethod=%s>" % ("%s.%s"%(self.__class__.__module__, self.__class__.__qualname__), self.name)
    def __str__(self):
        return "%s (%s)" % (self.name, ("%s.%s"%(self.__class__.__module__, self.__class__.__qualname__)))
    def run(self):
        return self.name

class test_C(TestCase):
    def test_1(self):
        print(1)
    def test_2(self):
        print(2)
    def test_3(self):
        print(3)
class test_C1(TestCase):
    def test_1(self):
        print(1)
    def test_2(self):
        print(2)
    def test_3(self):
        print(3)


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
   testC=test_C

   print(testC("name"))
   print(testC)
    # a=test
    # l=[]
    # print(a)
    # print(a.__class__)
    # def  is_callable(name):
    #     if name.startswith("test")  and  callable(getattr(a,name)):
    #         return getattr(a,name)
    # f=list(filter(is_callable,dir(a)))
    # l=[]
    # for  name  in f:
    #     print(getattr(a,name))
    #     l.append(getattr(a,name))
    # print(l)
    # suite=A
    # print(suite(l))







# A=TestSuite
# print(A)
# print(A([1,23,3,4,56]))

c=1
def fib(n):
    index = 0
    a = 0
    b = 1

    while index < n:
        yield b
        print(b)
        a,b = b, a+b
        index += 1
a=input("输入值：")
print([fib(a)])

def fun_inner():
    i = 0
    while True:
        i = yield i

def fun_outer():
    a = 0
    b = 1
    inner = fun_inner()
    inner.send(None)
    while True:
        a = inner.send(b)
        b = yield a

if __name__ == '__main__':
    outer = fun_outer()
    outer.send(None)
    for i in range(5):
        print(outer.send(i))


