from django.db import models
# Create your models here.

class CaseGroupFiles(models.Model):
    """用例文件夹"""
    name=models.CharField(max_length=255,verbose_name="用例文件夹名称")
    interfaceId=models.IntegerField(verbose_name="同步过来文件的id",null=True,db_index=True,)
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
    order = models.IntegerField(verbose_name="执行顺序",null=True,default=1)
    CaseGroupFilesId=models.ForeignKey("CaseGroupFiles",to_field="id",on_delete=models.SET_NULL,null=True,db_index=True,
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
    addEnv=models.TextField(verbose_name="新增环境变量操作",null=True)
    assertAction=models.TextField(verbose_name="断言",null=True)
    environmentId =models.ForeignKey("project.Environments",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="关联的环境变量id")
    attr=models.CharField(max_length=255,verbose_name="请求地址")
    status=models.IntegerField(choices=status_Choices,default=0,verbose_name="用例状态")
    detail=models.TextField(verbose_name="用例描述",null=True)
    isGlobalsHeader=models.IntegerField(default=0,verbose_name="全局请求头") #是否使用全局请求头，默认不使用 该字段用于后续扩展
    beforeAction=models.TextField(null=True,blank=True,verbose_name="前置操作")
    headers=models.TextField(null=True,blank=True,verbose_name="请求头")  #请求头数据
    data=models.TextField(null=True,blank=True,verbose_name="请求参数")  #请求参数
    afterAction=models.TextField(null=True,blank=True,verbose_name="后置操作")
    createTime=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    update_userId = models.ForeignKey("users.UserProfile", to_field="id", on_delete=models.SET_NULL, null=True,
                               related_name="up_name", verbose_name="创建人")
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    class Meta:
        db_table="case_file"

class CasePlan(models.Model):
    status_Choices=(
        (0,"未执行"),
        (1,"执行中"),
        (2,"已完成")
    )
    timed_timedId=(
        (0, "暂停"),
        (1, "有效"),
    )
    run_Choices=(
        (0, "手动执行"),
        (1, "定时执行"),
        (2, "轮询")
    )
    name=models.CharField(max_length=255,verbose_name="计划名称")
    cname=models.CharField(max_length=255,verbose_name="脚本名称")
    againScript=models.IntegerField(verbose_name="是否重新创建脚本")
    projectId=models.ForeignKey("project.ProjectList",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="项目id")
    userId = models.ForeignKey("users.UserProfile", to_field="id", on_delete=models.SET_NULL, null=True,related_name="c_name",verbose_name="创建人")
    status=models.IntegerField(choices=status_Choices,default=0,null=True,verbose_name="执行状态")
    runType=models.IntegerField(choices=run_Choices,default=0,verbose_name="执行方式")
    cron = models.CharField(max_length=255, verbose_name="cron定时表达式",null=True)
    CaseCount=models.IntegerField(null=True,verbose_name="用例数量")
    caseStartTime=models.DateTimeField(verbose_name="计划开始时间",null=True)
    caseEndTime = models.DateTimeField(verbose_name="计划结束时间", null=True)
    timedId=models.IntegerField(choices=timed_timedId,default=0,null=True,verbose_name="定时任务状态")
    taskId=models.IntegerField(null=True,verbose_name="定时任务Id")
    detail=models.TextField(verbose_name="计划描述",null=True)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    class Meta:
        db_table="case_plan"

class CaseResult(models.Model):
    userId = models.ForeignKey("users.UserProfile", to_field="id", on_delete=models.SET_NULL, null=True,related_name="cc_name",verbose_name="创建人")
    caseCount = models.IntegerField(null=True,default=1,verbose_name="用例数量")
    type=models.IntegerField(null=True,verbose_name="结果类别")   #1debug接口  2批量结果 3allrun结果
    result=models.TextField(null=True,verbose_name="测试结果")
    c_id=models.IntegerField(verbose_name="所属id")#type==1 传caseId   type==2传interfaceId   type==3传casePlanId
    assertSuccess=models.IntegerField(null=True, verbose_name="断言成功数量，扩展字段")
    assertFailed = models.IntegerField(null=True, verbose_name="断言失败数量，扩展字段")
    runFailed = models.IntegerField(null=True, verbose_name="执行失败数量，扩展字段")
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    class Meta:
        db_table="case_result"

class timedTask(models.Model):
    """该表关联计划表和 django_celery_beat_periodictask django_celery_beat_crontabschedule表
        定时任务停止则删除 django_celery_beat_crontabschedule定时和django_celery_beat_periodictask任务--以及修改CasePlan执行方式为手动
        重新启动 则新增--
        删除则 修改CasePlan执行方式---删除该表相关内容  以及 beat表两张表的呃逆荣
    """
    status_Choices = (
        (0, "暂停"),
        (1, "有效"),
    )
    taskName=models.TextField(null=True,verbose_name="任务名称")
    status = models.IntegerField(choices=status_Choices, default=0, null=True, verbose_name="执行状态")
    PeriodicTaskId=models.IntegerField(null=True,verbose_name="任务id")
    results=models.TextField(null=True,verbose_name="最近执行结果")
    #如果删除任务则需要联动删除这个
    casePlanId =models.ForeignKey("CasePlan",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="项目id",related_name="casePlanId_tt")
    userId = models.ForeignKey("users.UserProfile", to_field="id", on_delete=models.SET_NULL, null=True,related_name="userId_tt",verbose_name="创建人")
    projectId=models.ForeignKey("project.ProjectList",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="项目id")

    cron = models.CharField(max_length=255, verbose_name="cron定时表达式",null=True)
    detail=models.TextField(verbose_name="定时描述",null=True)
    taskId = models.IntegerField(null=True, verbose_name="定时任务Id")

    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table="django_celery_beat_task"



class SqlBox(models.Model):
    type_Choices = (
        (1, "MySql"),
        (2, "SqlSever"),
        (3,"Redis"),
        (4, "Oracle")
    )
    userId = models.ForeignKey("users.UserProfile", to_field="id", on_delete=models.SET_NULL, null=True,related_name="userId_SqlBox",verbose_name="创建人")
    projectId=models.ForeignKey("project.ProjectList",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="项目id",related_name="projectId_SqlBox")
    name = models.CharField(verbose_name="变量名",max_length=255)
    type = models.IntegerField(choices=type_Choices,default=1,verbose_name="数据库类型")
    host = models.CharField(verbose_name="主机地址",max_length=255)
    port = models.CharField(verbose_name="端口",max_length=255)
    database=models.CharField(verbose_name="数据库名称",max_length=255)
    userName = models.CharField(verbose_name="用户名",max_length=255)
    passWord = models.CharField(verbose_name="密码",max_length=255)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    detail=models.TextField(verbose_name="描述",null=True)

    class Meta:
        db_table="sql_box"
class SqlStatement(models.Model):
    type_Choices = (
        (1, "查"),
        (2, "改"),
        (3, "增"),
        (3, "删")
    )
    BoxId=models.ForeignKey("SqlBox",to_field="id",on_delete=models.SET_NULL,null=True,related_name="boxId_ss")
    userId = models.ForeignKey("users.UserProfile", to_field="id", on_delete=models.SET_NULL, null=True,
                               related_name="userId_ss", verbose_name="创建人")
    projectId = models.ForeignKey("project.ProjectList", to_field="id", on_delete=models.SET_NULL, null=True,
                                  verbose_name="项目id")
    saveResultChoice=models.TextField(verbose_name="是否保存到环境变量",null=True)
    envId=models.ForeignKey("project.Environments",to_field="id",on_delete=models.SET_NULL,null=True,verbose_name="关联的环境变量id")
    SqlActionResults=models.TextField(verbose_name="sql结果处理",null=True)
    type = models.IntegerField(choices=type_Choices,default=1,verbose_name="执行语句类型")
    name = models.CharField(verbose_name="数据库连接名", max_length=255)
    sql = models.TextField(verbose_name="sql语句",null=True)
    createTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updateTime = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    detail=models.TextField(verbose_name="描述",null=True)

    class Meta:
        db_table="sql_statement"

