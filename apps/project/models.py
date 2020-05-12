from django.db import models
# Create your models here.

class ProjectList(models.Model):
    """项目列表"""
    name=models.CharField(max_length=20,verbose_name="项目名称")
    dev_attr=models.CharField(max_length=100,verbose_name="开发地址")
    test_attr=models.CharField(max_length=100,verbose_name="测试地址")
    product_attr=models.CharField(max_length=100,verbose_name="生产地址")
    create_time=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    user=models.ForeignKey("users.UserProfile",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="创建用户id")
    class Meta:
        db_table= "project_list"



class PostMethods(models.Model):
    """请求方法"""
    name=models.CharField(max_length=10,verbose_name="请求方法名称")
    class Meta:
        db_table= "post_methods"

class PostType(models.Model):
    """请求类型"""

    name = models.CharField(max_length=100, verbose_name="请求类型名称")
    class Meta:
        db_table= "post_type"

class ResType(models.Model):
    """返回类型"""
    name = models.CharField(max_length=10, verbose_name="返回类型名称")
    class Meta:
        db_table= "res_type"

class InterfaceFilesName(models.Model):
    """文件夹"""
    name=models.CharField(max_length=100)
    project_id=models.ForeignKey("ProjectList",on_delete=models.SET_NULL,null=True,related_name="file_project",verbose_name="所属项目id")
    class Meta:
        db_table="interface_files_name"

class InterfaceFiles(models.Model):
    """文档列表"""

    project=models.ForeignKey("ProjectList", to_field="id", on_delete=models.SET_NULL,null=True, related_name="project_id", verbose_name="所属项目id")
    file=models.ForeignKey("InterfaceFilesName",to_field="id",on_delete=models.SET_NULL,null=True,related_name="files_name",verbose_name="关联接口文件id")
    create_user=models.ForeignKey("users.UserProfile", to_field="id", on_delete=models.SET_DEFAULT, default=None, related_name="create_user_id", verbose_name="创建用户")
    filesName=models.CharField(max_length=255, verbose_name="接口文档名称")

    post_methods=models.ForeignKey("PostMethods",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="该接口请求方法id")
    post_type=models.ForeignKey("PostType",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="该接口请求类型id")

    post_attr=models.CharField(max_length=255,verbose_name="请求地址",null=True)
    interface_detail = models.CharField(max_length=255, verbose_name="接口描述",null=True)
    mock_attr=models.CharField(max_length=255,verbose_name="mock地址",null=True)
    mock_type=models.CharField(max_length=10,verbose_name="返回数据类型",null=True)
    mock_data=models.TextField(verbose_name="mock自定义数据",null=True)
    post_header=models.TextField(verbose_name="请求头",null=True)
    post_data = models.TextField( verbose_name="请求数据",null=True)
    res_header = models.TextField( verbose_name="返回头部",null=True)
    res_data = models.TextField( verbose_name="返回数据",null=True)

    res_type=models.ForeignKey("ResType",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="该接口返回方法id")
    create_time=models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time=models.DateTimeField(auto_now=True, verbose_name="更新时间")
    class Meta:
        db_table= "interface_files"



class Environments(models.Model):
    name=models.CharField(verbose_name="环境名称",max_length=128,null=True)
    value=models.TextField(verbose_name="值",null=True)
    is_eg=models.IntegerField(verbose_name="类型")  #1是环境变量  2是全局变量
    create_time=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    update_time=models.DateTimeField(auto_now=True,verbose_name="更新时间")

    class Meta:
        db_table= "environment_s"




class Menu(models.Model):
    name = models.CharField(verbose_name='名称', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32, null=True, blank=True)
    first = models.BooleanField(verbose_name='是否为一级菜单', default=False)
    url = models.CharField(verbose_name='路由(包含正则表达式)', max_length=32)
    parent = models.ForeignKey('self',to_field="id" ,null=True, blank=True, on_delete=models.SET_NULL,related_name="pc") # on_delete 是否级联删除
    menu_display_choices = (
        (1, '显示'), (2, '隐藏')
    )
    display = models.IntegerField(choices=menu_display_choices, default=1)

    class Meta:
        verbose_name_plural = '菜单管理'

    def __str__(self):
        return self.name