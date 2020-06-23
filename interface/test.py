from log.logFile import logger as logs
import  logging,time
import sys,io,os,django

os.environ.setdefault("DJANGO_SETTINGS_MODULE","besettest.settings")
django.setup()
from django_redis import get_redis_connection  as conn
# conn = conn('default')
logRedis=conn("log")
logRedis.rpush("log:user_id_time1","log")



class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self,fp,projectId,userId,runTime):
        self.projectId = projectId
        self.userId = userId
        self.runTime = runTime
        self.start=sys.stdout
        self.logRedis = conn("log")
        self.fp = fp
    def write(self, s):
        self.fp.write(s)
        key="%s_%s_%s"%(self.projectId,self.userId,self.runTime)
        self.logRedis.rpush("log:%s"%key, s)
        sys.stdout = self.start
    def writelines(self, lines):
        self.fp.writelines(lines)
    def flush(self):
        self.fp.flush()
class StartMethod(object):
    def __init__(self, projectId, userId, runTime):
        self.projectId = projectId
        self.userId = userId
        self.runTime = runTime
        self.stdout_redirector = OutputRedirector(sys.stdout, self.projectId, self.userId, self.runTime)
        self.stderr_redirector = OutputRedirector(sys.stderr, self.projectId, self.userId, self.runTime)
        self.startTest()
        self.logger=logs(self.__class__.__module__)
    def __call__(self, *args, **kwargs):
        return self.c()
    def startTest(self):
        self.outputBuffer = io.StringIO()
        self.stdout_redirector.fp = self.outputBuffer
        self.stderr_redirector.fp = self.outputBuffer
        # self.stdout0 = sys.stdout  # 记录标准输出原始位置
        # self.stderr0 = sys.stderr
        sys.stdout = self.stdout_redirector
        sys.stderr = self.stderr_redirector

        sys.stdout = self.stdout_redirector
        sys.stderr = self.stderr_redirector

    def c(self):

        self.logger.info("log")
        time.sleep(0.1)
        print("这是print的内容")
        time.sleep(0.1)
        self.logger.info("log")
        time.sleep(0.1)
        self.logger.info("执行前置操作")
        time.sleep(0.1)
        self.logger.info("log1")
        time.sleep(0.1)
        self.logger.info("log2")
        time.sleep(0.1)
        self.logger.info("log3")
        time.sleep(0.1)
        self.logger.info("log4")
        time.sleep(0.1)
        self.logger.info("log5")
        time.sleep(0.1)



a=StartMethod("这是项目","这是所属用例3","这是时间")
a.c()
print(21212121)
