# # from django.test import TestCase
# #
# # # Create your tests here.
# # import  os
# # import  sys,django
# # # print(os.path.abspath("./"))
# # # print(os.getcwd())
# # # A='besettest.py'
# # # B="interface\\testFiles"
# # #
# # # c=os.path.splitext(A)
# # # print(c)
# # #
# # #
# # #
# # # #
# # # # print(sys.path)
# # # # print(os.path)
# #
# # # print(a )
# # # print(os.path.join(a, '__init__.py'))
# # # # a=os.path.isfile(os.path.join(case_dir, '__init__.py'))
# # #
# # # # print(sys.modules)
# # # # # b=sys.modules[a]
# # # # # print(b)
# # # a="interface.testFiles"
# # # try:
# # #     __import__(a)
# # #
# # # except ImportError as f:
# # #     print(f)
# # # else:
# # #     print("sys.modules",sys.modules)
# # #     print("start_dir.split('.')[0] ",a.split('.')[0] )
# # #
# # #     the_module = sys.modules[a]  # 这里是如果我们导入成功--就走这里-取出start_dir导入的赋值给the_module
# # #     print("the_module.__file__)", the_module.__file__)
# # #     top_part = a.split('.')[0]
# # #     print("the_module",the_module)
# # #     c=the_module.__spec__
# # #     print("he_module.__spec__.submodule_search_locations",the_module.__spec__.submodule_search_locations)
# # #     print("c.name",c.name)
# # #     print("c.loader",c.loader)
# # #     print("c.origin",c.origin)
# # #     print()
# # #     print("the_module.__path__",the_module.__path__)
# # #     path='E:\\PyFiles\\Besettest\\besettest\\interface'
# # #     oo=path.split(the_module.__name__.replace(".", os.path.sep))[0]
# # #     print(the_module.__name__.replace(".", os.path.sep))
# # #     print(oo,"00")
# # #     # ModuleSpec(name='interface', loader= < _frozen_importlib_external.SourceFileLoader
# # #     # object
# # #     # at
# # #     # 0x0000000003D6E780 >, origin = 'E:\\PyFiles\\Besettest\\besettest\\interface\\__init__.py', submodule_search_locations = [
# # #     #     'E:\\PyFiles\\Besettest\\besettest\\interface'])
# # #     print("导入模块的绝对路径",os.path.abspath(
# # #                        os.path.dirname((the_module.__file__))))
# # #     print(top_part)
# # #     module = sys.modules["interface"]
# # #     print(module)
# # #
# # #     full_path = os.path.abspath(module.__file__)
# # #     print(module.__file__)
# # #     print(full_path)
# # #     print(os.path.basename(full_path))
# # #     print(os.path.dirname(os.path.dirname(full_path)))
# # #     print(dir("E:\\PyFiles\\Besettest\\besettest\\interface\\testFiles\\againScript2'"))
# # #     print(os.path.isabs("..\.."))
# #
# #
# # #     path1="E:\\PyFiles\\Besettest\\besettest\\interface\\testFiles"
# # #     path2="E:\\PyFiles\\Besettest\\besettest\\interface\\result"
# # #     _relpath = os.path.relpath(path1, path2)
# # #     print(_relpath )
# # #     assert not os.path.isabs(_relpath)
# # #     name = _relpath.replace(os.path.sep, '.')
# # #     print(name)
# # #     print("./tests")
# # #     print(set())
# # #     print(type(set()))
# # #     s=set()
# # #     s={1,2,3,4,1}
# # #     print(s)
# # # from fnmatch import fnmatch
# # # a=fnmatch("case.py","*.py")
# # # print(a)
#
# # # print(os.path.basename("E:\\PyFiles\\Besettest\\besettest\\interface\\result\\aa.py"))
# # # sys.path.insert(0,os.path.abspath("E:\\PyFiles\\Besettest\\besettest\\interface\\testFiles"))
# # # __import__('againScript2')
# # # print(sys.modules["againScript2"].__file__)
# # # print(sys.modules["againScript2"].__name__)
# # # print(os.path.realpath(os.path.abspath(sys.modules["againScript2"].__file__)))
# # # print(sys.path)
# # print(os.path.dirname(__file__))
# # print(os.path.basename(r"E:\PyFiles\Besettest\besettest\interface\testFiles\againScript2.py"))
# # paths=os.listdir(r"E:\PyFiles\Besettest\besettest\interface\testFiles")
# # print(os.path.basename(r"E:\PyFiles\Besettest\besettest\interface\testFiles"))
# # from  unittest import util
# # # def strclass(cls):
# # #     return "%s.%s" % (cls.__module__, cls.__qualname__)
# # class  A():
# #     def __init__(self):
# #         self.a="test"
# #         self.b="dev"
# #     def __repr__(self):
# #         return "suite[class=%s<21>]"%(util.strclass(self.__class__))
# #     def b(self):
# #         pass
# #
# # a=A()
# # print(a)
# # print(a.a)
# # print(a.__module__,A.b.__qualname__)
# # print(a.__class__)
#
#
# from case import testss
# from  case.testss import TestCase
# import sys,django,os
# from unittest import case
# suiteClass=testss.A
# TestResult=testss.TestResult
# os.environ.setdefault("DJANGO_SETTINGS_MODULE","besettest.settings")
# django.setup()
# sys.path.insert(0,os.path.abspath(r"E:\PyFiles\DjangoBesettest\apps\case"))
# __import__('testss')
# Module=sys.modules["testss"]
# print(sys.modules)
# print(Module,"Module")
# testMethodPrefix="test"
# l=[]
# print(dir(Module))
# for  testClass in dir(Module):
#     # if  testClass.startswith("test"):
#     obj=getattr(Module,testClass)   #模块的类属性
#     if isinstance(obj, type):
#         print("1111")
#         def isTestMethod(attrname, testCaseClass=obj,
#                          prefix=testMethodPrefix):
#             return attrname.startswith(prefix) and \
#                 callable(getattr(testCaseClass, attrname))
#
#         testCase=list(filter(isTestMethod, dir(obj)))
#         print("testCase",testCase)
#         # List=[]
#         # for  name in testCase:
#         #     List.append(getattr(obj,name))
#         List=map(obj,testCase)
#         # for  a  in  List:
#         #     print(a)
#         b=suiteClass(List)
#
#         l.append(b)
# print(l)
# suite=suiteClass(l)
# print(l)
# for  a  in  suite:
#     print(a)
#     for index, test in enumerate(a):
#         print(index,test)
#
#         # a = list(map(obj, testCase))
#         # print(suiteClass(a))
# # <case.testss.A tests=[<testss.test_C testMethod=test_1>, <testss.test_C testMethod=test_2>, <testss.test_C testMethod=test_3>]>
#

#
# def  a(n):
#     testList=b(n)
#     return testList
#
# def  b(n,m=1):
#     print("执行第%s次"%m)
#     for a in range(n):
#         if not divmod(a,2)[1] and a!=0:
#             print(a)
#             yield a
#             if divmod(a,3)[1]:
#                 m =m+1
#                 yield from b(a,m)
#
# print(list(a(7)))
#
#
# def  test():
#     a=0
#     b=1
#     for  c in  range(10):
#         a,b = b,a+b
#         yield a
#
# print(list(test()))


class  A(object):
    def __init__(self,test):
        self.test=test

    def __call__(self, *args, **kwargs):
        return self.add()
    def add(self):
        return self.test
    def add1(self):
        return 2222
import sys
a=sys.modules[A.__module__]
moduleClass=dir(a)
print(moduleClass)
obj=getattr(a,"A")
print(dir(obj))

fileName=list(filter(lambda x:x.startswith("add"),dir(obj)))
print(fileName)




print(list(map(obj,fileName)))
print(A(1))
print(getattr(obj("test"),"add")())
print("_________________________________________________________________")

class   test2():  #这个也是suite集合生成用的东西
    def __call__(self, *args, **kwargs):
        return self.add(*args, **kwargs)
    def add(self,a,b):
        return a+b
print(a)