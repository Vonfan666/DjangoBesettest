# from django.test import TestCase
#
# # Create your tests here.
# import  os
# import  sys,django
# # print(os.path.abspath("./"))
# # print(os.getcwd())
# # A='besettest.py'
# # B="interface\\testFiles"
# #
# # c=os.path.splitext(A)
# # print(c)
# #
# #
# #
# # #
# # # print(sys.path)
# # # print(os.path)
#
# # print(a )
# # print(os.path.join(a, '__init__.py'))
# # # a=os.path.isfile(os.path.join(case_dir, '__init__.py'))
# #
# # # print(sys.modules)
# # # # b=sys.modules[a]
# # # # print(b)
# # a="interface.testFiles"
# # try:
# #     __import__(a)
# #
# # except ImportError as f:
# #     print(f)
# # else:
# #     print("sys.modules",sys.modules)
# #     print("start_dir.split('.')[0] ",a.split('.')[0] )
# #
# #     the_module = sys.modules[a]  # 这里是如果我们导入成功--就走这里-取出start_dir导入的赋值给the_module
# #     print("the_module.__file__)", the_module.__file__)
# #     top_part = a.split('.')[0]
# #     print("the_module",the_module)
# #     c=the_module.__spec__
# #     print("he_module.__spec__.submodule_search_locations",the_module.__spec__.submodule_search_locations)
# #     print("c.name",c.name)
# #     print("c.loader",c.loader)
# #     print("c.origin",c.origin)
# #     print()
# #     print("the_module.__path__",the_module.__path__)
# #     path='E:\\PyFiles\\Besettest\\besettest\\interface'
# #     oo=path.split(the_module.__name__.replace(".", os.path.sep))[0]
# #     print(the_module.__name__.replace(".", os.path.sep))
# #     print(oo,"00")
# #     # ModuleSpec(name='interface', loader= < _frozen_importlib_external.SourceFileLoader
# #     # object
# #     # at
# #     # 0x0000000003D6E780 >, origin = 'E:\\PyFiles\\Besettest\\besettest\\interface\\__init__.py', submodule_search_locations = [
# #     #     'E:\\PyFiles\\Besettest\\besettest\\interface'])
# #     print("导入模块的绝对路径",os.path.abspath(
# #                        os.path.dirname((the_module.__file__))))
# #     print(top_part)
# #     module = sys.modules["interface"]
# #     print(module)
# #
# #     full_path = os.path.abspath(module.__file__)
# #     print(module.__file__)
# #     print(full_path)
# #     print(os.path.basename(full_path))
# #     print(os.path.dirname(os.path.dirname(full_path)))
# #     print(dir("E:\\PyFiles\\Besettest\\besettest\\interface\\testFiles\\againScript2'"))
# #     print(os.path.isabs("..\.."))
#
#
# #     path1="E:\\PyFiles\\Besettest\\besettest\\interface\\testFiles"
# #     path2="E:\\PyFiles\\Besettest\\besettest\\interface\\result"
# #     _relpath = os.path.relpath(path1, path2)
# #     print(_relpath )
# #     assert not os.path.isabs(_relpath)
# #     name = _relpath.replace(os.path.sep, '.')
# #     print(name)
# #     print("./tests")
# #     print(set())
# #     print(type(set()))
# #     s=set()
# #     s={1,2,3,4,1}
# #     print(s)
# # from fnmatch import fnmatch
# # a=fnmatch("case.py","*.py")
# # print(a)

# # print(os.path.basename("E:\\PyFiles\\Besettest\\besettest\\interface\\result\\aa.py"))
# # sys.path.insert(0,os.path.abspath("E:\\PyFiles\\Besettest\\besettest\\interface\\testFiles"))
# # __import__('againScript2')
# # print(sys.modules["againScript2"].__file__)
# # print(sys.modules["againScript2"].__name__)
# # print(os.path.realpath(os.path.abspath(sys.modules["againScript2"].__file__)))
# # print(sys.path)
# print(os.path.dirname(__file__))
# print(os.path.basename(r"E:\PyFiles\Besettest\besettest\interface\testFiles\againScript2.py"))
# paths=os.listdir(r"E:\PyFiles\Besettest\besettest\interface\testFiles")
# print(os.path.basename(r"E:\PyFiles\Besettest\besettest\interface\testFiles"))
# from  unittest import util
# # def strclass(cls):
# #     return "%s.%s" % (cls.__module__, cls.__qualname__)
# class  A():
#     def __init__(self):
#         self.a="test"
#         self.b="dev"
#     def __repr__(self):
#         return "suite[class=%s<21>]"%(util.strclass(self.__class__))
#     def b(self):
#         pass
#
# a=A()
# print(a)
# print(a.a)
# print(a.__module__,A.b.__qualname__)
# print(a.__class__)


from case import testss

import sys,django,os
from unittest import case
suiteClass=testss.TestSuite

os.environ.setdefault("DJANGO_SETTINGS_MODULE","besettest.settings")
django.setup()
sys.path.insert(0,os.path.abspath("E:\\PyFiles\\Besettest\\besettest\\interface\\testFiles"))
__import__('againScript2')
Module=sys.modules["againScript2"]
print(Module)
testMethodPrefix="test"
for  testClass in dir(Module):
    obj=getattr(Module,testClass,None)
    if isinstance(obj, type) and issubclass(obj, case.TestCase):

        def isTestMethod(attrname, testCaseClass=obj,
                         prefix=testMethodPrefix):
            return attrname.startswith(prefix) and \
                callable(getattr(testCaseClass, attrname))
        testCase=list(filter(isTestMethod, dir(obj)))
        print(testCase)
        a=list(map(obj,testCase))
        suite=suiteClass(a)
        print(suite)
