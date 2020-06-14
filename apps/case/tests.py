from django.test import TestCase

# Create your tests here.
import  os
import  sys
# print(os.path.abspath("./"))
# print(os.getcwd())
# A='besettest.py'
# B="interface\\testFiles"
#
# c=os.path.splitext(A)
# print(c)
#
#
#
# #
# # print(sys.path)
# # print(os.path)
a = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), r"interface/testFiles")
a=os.path.abspath(a)
# print(a )
# print(os.path.join(a, '__init__.py'))
# # a=os.path.isfile(os.path.join(case_dir, '__init__.py'))
#
# # print(sys.modules)
# # # b=sys.modules[a]
# # # print(b)
a="interface.testFiles"
try:
    __import__(a)

except ImportError as f:
    print(f)
else:
    print("sys.modules",sys.modules)
    print("start_dir.split('.')[0] ",a.split('.')[0] )

    the_module = sys.modules[a]  # 这里是如果我们导入成功--就走这里-取出start_dir导入的赋值给the_module
    print("the_module.__file__)", the_module.__file__)
    top_part = a.split('.')[0]
    print("the_module",the_module)
    c=the_module.__spec__
    print("he_module.__spec__.submodule_search_locations",the_module.__spec__.submodule_search_locations)
    print("c.name",c.name)
    print("c.loader",c.loader)
    print("c.origin",c.origin)
    print()
    print("the_module.__path__",the_module.__path__)
    path='E:\\PyFiles\\Besettest\\besettest\\interface'
    oo=path.split(the_module.__name__.replace(".", os.path.sep))[0]
    print(the_module.__name__.replace(".", os.path.sep))
    print(oo,"00")
    # ModuleSpec(name='interface', loader= < _frozen_importlib_external.SourceFileLoader
    # object
    # at
    # 0x0000000003D6E780 >, origin = 'E:\\PyFiles\\Besettest\\besettest\\interface\\__init__.py', submodule_search_locations = [
    #     'E:\\PyFiles\\Besettest\\besettest\\interface'])
    print("导入模块的绝对路径",os.path.abspath(
                       os.path.dirname((the_module.__file__))))
    print(top_part)
    module = sys.modules["interface"]
    print(module)

    full_path = os.path.abspath(module.__file__)
    print(module.__file__)
    print(full_path)
    print(os.path.basename(full_path))
    print(os.path.dirname(os.path.dirname(full_path)))
    print(dir("E:\\PyFiles\\Besettest\\besettest\\interface\\testFiles\\againScript2'"))