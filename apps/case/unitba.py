#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年06月17日00时50分44秒



class TestCase():
    def __init__(self,name="test"):
        self.name=name
    def __repr__(self):
        return "<%s testMethod=%s>" % ("%s,%s"%(self.__class__.__module__, self.__class__.__qualname__), self.name)
    def  a(self):
        print(self.name)
    def b(self):
        print(self.name)
class test_C(TestCase):

        # return "<%s at '假装是一个内存地址'>" % ("%s.%s" % (self.__class__.__module__, self.__class__.__qualname__))
    def test_1(self):
        pass
    def test_2(self):
        pass
    def test_3(self):
        pass

# if __name__ == "__main__":
#     print(test_C)
#     print(test_C())


class BaseTestSuite(object):
    def __init__(self,tests=()):
        # self.b=1
        self.tests=[]
        self.add(tests)
    def __repr__(self):
        return "<%s tests=%s>"%(self.__class__.__module__,self.tests)
    # def __call__(self, *args, **kwds):
    #     return self.run(*args, **kwds)
    # def __eq__(self, other):
    #     if not isinstance(other, self.__class__):
    #         return NotImplemented
    #     return list(self) == list(other)
    # def __iter__(self):
    #     return iter(self.tests)

    # def run(self,tests):
    #     print(1)
    #     for index, test in enumerate(self):
    #         return index,test
    def  add(self,tests):
        for a  in tests:
            self.tests.append(a)
class TestSuite(BaseTestSuite):
    pass










