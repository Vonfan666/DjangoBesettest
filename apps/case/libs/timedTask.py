from  rest_framework.views import APIView,status
from libs.api_response import APIResponse
from  users.models import UserProfile
from case import models,serializers
import pytz,time,json
from django_celery_beat.models import PeriodicTask,CrontabSchedule

class TimedTask(APIView):
    """定时任务
        新建/编辑计划时如果设置了定时-这里就会管理任务表和 beat系列表
        1. Minutes （分）
        2. Hours （时）
        3. Day-of-Month （天）
        4. Month （月）
        5. Day-of-Week （周）
    """

    def cronChange(self):
        timeList = self.data["cron"].split(" ")
        if timeList[4] == "?":
            timeList[4] = "*"
        return timeList

    #每次选择定时执行更新时，都需要先删除老的任务-然后创建新的任务

    def create(self, cronTime):
        """创建定时策略以及任务"""
        PeriodicTask_id = PeriodicTask.objects.filter(id=self.data["taskId"])
        self.isTask(self.data["taskId"],PeriodicTask_id)  # 判断任务里面是否存在存在这个id，


        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=cronTime[0],
            hour=cronTime[1],
            day_of_week=cronTime[2],  # 可出现", - * / ? L C #"四个字符，有效范围为1-7的整数或SUN-SAT两个范围。1表示星期天，2表示星期一， 依次类推
            day_of_month=cronTime[3],
            month_of_year=cronTime[4],  # 可出现", - * / ? L W C"八个字符，有效范围为0-31的整数
            timezone=pytz.timezone('Asia/Shanghai'),
        )
        if not PeriodicTask_id:
            self.addTask(schedule)
        else:
            obj = PeriodicTask.objects.get(id=self.data["taskId"])
            if obj.enabled:  # 如果任务还在执行中--需要先停止任务--然后在修改celery所属的定时
                self.stopTask(self.data["taskId"])
                PeriodicTask.objects.filter(id=self.data["taskId"]).update(crontab=schedule)
                self.startTask(self.data["taskId"])
            else:
                PeriodicTask.objects.filter(id=self.data["taskId"]).update(crontab=schedule)
    def isTask(self, task_id,PeriodicTask_id=None):
        """celery 存在任务，则先删除原来的任务，然后添加新的任务"""
        if task_id and PeriodicTask_id:  #计划表准备任务Id
            self.update(task_id)
            # self.deleteTask(task_id)  #删除原来的任务


    def update(self, task_id):
        """判断是否修改任务状态"""
        if int(self.data["timedId"]) == 1:  #有效的任务
            self.startTask(task_id)
        if int(self.data["timedId"]) == 0:  #暂停的人
            self.stopTask(task_id)

    def addTask(self, schedule):  # 添加任务并同步id到计划表
        task_obj=PeriodicTask.objects.create(
            crontab=schedule,
            name=self.name,
            task="case.tasks.timedTask",
            args=json.dumps([self.data]),
        )

        task_id = task_obj.id # 获取taskId
        models.CasePlan.objects.filter(id=self.data["id"]).update(taskId=task_id)  # 将创建的任务Id插入计划表
        self.update(task_id)  # 判断任务暂停还是执行
        # self.createTask(task_id)  #将数据同步到自己的任务表中
        return task_id
    def stopTask(self, task_id):  # 暂停任务
        obj = PeriodicTask.objects.get(id=task_id)
        obj.enabled = False
        obj.save()

    def startTask(self, task_id):  # 开始任务
        obj = PeriodicTask.objects.get(id=task_id)
        obj.enabled = True
        obj.save()

    def deleteTask(self, task_id):  # 删除任务
        try:
            obj = PeriodicTask.objects.get(id=task_id)
            obj.enabled = False
            obj.delete()
            self.clear_CrontabSchedule(obj)
        except:
            return

    def task(self, data):
        if data["runType"]==1:
            timeStr = time.strftime("%Y%m%d%H%M%S", time.localtime())
            self.data = data
            self.name = 'timedTask_%s_%s_%s' % (self.data["id"], self.data["userId"], timeStr)
            cronTime = self.cronChange()
            self.create(cronTime)
            # if not models.timedTask.objects.filter(planId_id=self.data["id"]):
            #     self.create(cronTime)  # 传整个data 和定时策略时间
        if data["timedId"]==1 and data["runType"]==0 :  #如果手动执行。。就把关联的任务改为暂停
            models.CasePlan.objects.filter(id=data["id"]).update(timedId=0)
            if data["taskId"]:
                self.stopTask(data["taskId"])  #暂停任务。。。且将定时状态改为无效
    def createTask(self, task_id):
        """操作任务时关联三张表计划表/自己的任务表/celery的任务表"""
        # 先判断该表是否存在
        user = UserProfile.objects.get(id=self.data["userId"])
        plan = models.CasePlan.objects.get(id=self.data["id"])
        data = {
            "PeriodicTaskId": task_id,
            "cron": self.data["cron"],
            "userId": user,
            "planId": plan,
        }
        models.timedTask.objects.create(**data)

    def clear_CrontabSchedule(self,obj):
        """当定时中不存在任务时，则删除定时"""
        CId=obj.crontab_id
        t=PeriodicTask.objects.filter(crontab_id=CId)
        if not t:
            CrontabSchedule.objects.get(id=CId).delete()


class myTimedTask(TimedTask):
    """
    1.task 表创建数据
    2.celery系列表创建数据
    3.增删改查
    """

    def createMyTask(self, cronTime):
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=cronTime[0],
            hour=cronTime[1],
            day_of_week=cronTime[2],  # 可出现", - * / ? L C #"四个字符，有效范围为1-7的整数或SUN-SAT两个范围。1表示星期天，2表示星期一， 依次类推
            day_of_month=cronTime[3],
            month_of_year=cronTime[4],  # 可出现", - * / ? L W C"八个字符，有效范围为0-31的整数
            timezone=pytz.timezone('Asia/Shanghai'),
        )
        return schedule
    def updateMyTask(self,data):
        status = data["status"]["id"]
        task_id = data["taskId"]
        self.data=data
        cronTime = self.cronChange()
        schedule=self.createMyTask(cronTime)
        obj=PeriodicTask.objects.get(id=task_id)
        if int(obj.crontab_id)!=int(schedule.id):
            if obj.enabled:
                self.stopTask(task_id)
                obj.crontab=schedule
                obj.save()
            else:
                obj.crontab = schedule
                obj.save()
        if status:
            self.startTask(task_id)
        else:
             self.stopTask(task_id)
    def selectMyTask(self,id):
        pass
    def deleteMyTask(self,task_id):
        self.deleteTask(task_id)
    def addTask(self, schedule):  # 添加任务并同步id到计划表

        task_obj=PeriodicTask.objects.create(
            crontab=schedule,
            name=self.name,
            task="case.tasks.timedTask",
            args=json.dumps([self.data]),
        )
        # task_obj = PeriodicTask.objects.get(name=self.name)  # 根据唯一的任务名获取创建的对象
        task_id = task_obj.id # 获取taskId

        self.update(task_id)  # 判断任务暂停还是执行
        # self.createTask(task_id)  #将数据同步到自己的任务表中
        return task_id
    def  run(self,data):
        self.data=data
        timeStr = time.strftime("%Y%m%d%H%M%S", time.localtime())
        cronTime=self.cronChange()
        self.name="%s_%s_%s"%(self.data["taskName"],self.data["userId"],timeStr)
        task_id=self.addTask(self.createMyTask(cronTime))
        models.timedTask.objects.filter(id=int(self.data["t_id"])).update(taskId=int(task_id)) #将celery任务Id同步到自己的表