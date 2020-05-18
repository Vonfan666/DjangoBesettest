from log.logFile import logger

logger=logger(__file__)
logger.info("另一个文件夹")
class Dog():
    '''这是一条狗'''
    dang='共产党'
    def __init__(self,name1,age1,gender1): #self代表init实例本身,实际上他的作用就是在接受参数转化为字典
        print('我是初始化函数')
        self.name=name1 #表示给实例赋予了一个name属性，同时接受一个name1的变量
        self.age=age1
        self.gender=gender1

    def  foo(self):  #函数属性
        print('这是第一个方法%s'%self.name)
    def  coo(self):
        print('这是第二个方法')

p1=Dog('cao','ri','nima')  #一运行，他就自动找init方法，将变量传到init

print(p1)
print(p1.__dict__) #{'name': 'cao', 'age': 'ri', 'gender': 'nima'}

print(p1.__dict__['name']) #cao
print(p1.name) #cao   和上面方法一样

print(p1.dang)

'''实例只有数据属性，没有函数属性'''
'''由一个类产生的实例，这个实例可以调用类属性，但是类属性肯定是访问不鸟实例属性（也就是那个字典）'''

Dog.foo(p1) #这是第一个方法cao
p1.foo()
print(11)
a=getattr(Dog,"foo",None)


class ListModelMixin:
    def  list(self,requests,*args,**kwargs):

        return self.__class__.__name__

class B(ListModelMixin):
    queryset=1
    def cao(self):
        pass

    def a(self):
        pass
    def get_queryset(self):
        a=1
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )
        print(a,"asdsdsada")
B().get_queryset()

print(ListModelMixin().list(111))
