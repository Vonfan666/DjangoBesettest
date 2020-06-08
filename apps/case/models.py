from django.db import models

# Create your models here.

class CaseGroupFiles(models.Model):
    """用例文件夹"""
    name=models.CharField(max_length=255,verbose_name="用例文件夹名称")
    interfaceId=models.IntegerField(verbose_name="同步过来文件的id",null=True)
    projectId=models.ForeignKey("project.ProjectList",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="项目id")
    userId=models.ForeignKey("users.UserProfile",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="创建用户id")
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updateTime=models.DateTimeField(auto_now=True,verbose_name="更新时间")
    class Meta:
        db_table="case_group_files"
class CaseGroup(models.Model):
    """  接口名称
    新建接口文档时这里就需要新增一个---前端加一个按钮是否同步接口文档分类"""
    name=models.CharField(max_length=255,verbose_name="接口名称")
    order = models.IntegerField(verbose_name="执行顺序",null=True)
    CaseGroupFilesId=models.ForeignKey("CaseGroupFiles",to_field="id",on_delete=models.SET_NULL,null=True,
                                        verbose_name="所属用例文件",related_name="idCaseGroupFiles")
    projectId = models.ForeignKey("project.ProjectList", to_field="id", on_delete=models.SET_NULL, null=True,
                                  verbose_name="项目id")
    userId = models.ForeignKey("users.UserProfile", to_field="id", on_delete=models.SET_NULL, null=True,
                               verbose_name="创建用户id")
    createTime=models.DateTimeField(auto_now_add=True,verbose_name="更新时间")
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    class Meta:
        db_table="case_group"
class CaseFile(models.Model):
    """用例管理"""
    status_Choices=(
        (0, "未完成"),
        (1,"已完成"),
    )
    name=models.CharField(max_length=255,verbose_name="用例名称")
    order = models.IntegerField(verbose_name="执行顺序")
    userId = models.ForeignKey("users.UserProfile", to_field="id", on_delete=models.SET_NULL, null=True,related_name="u_name",verbose_name="创建人")
    CaseGroupId=models.ForeignKey("CaseGroup",to_field="id",on_delete=models.SET_NULL,null=True,related_name="IdCaseGroup",verbose_name="所属接口用例")

    postMethod = models.ForeignKey("project.PostMethods",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="请求方法")
    dataType = models.ForeignKey("project.PostType", to_field="id", on_delete=models.SET_NULL, null=True,
                                 verbose_name="请求数据类型")
    environmentId =models.ForeignKey("project.Environments",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="关联的环境变量id")
    attr=models.CharField(max_length=255,verbose_name="请求地址")
    status=models.IntegerField(choices=status_Choices,default=0,verbose_name="用例状态")
    detail=models.TextField(verbose_name="用例描述",null=True)
    isGlobalsHeader=models.IntegerField(default=0,verbose_name="全局请求头") #是否使用全局请求头，默认不使用 该字段用于后续扩展
    headers=models.TextField(null=True,blank=True,verbose_name="请求头")  #请求头数据
    data=models.TextField(null=True,blank=True,verbose_name="请求参数")  #请求参数

    createTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    class Meta:
        db_table="case_file"