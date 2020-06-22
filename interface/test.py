from log.logFile import logger as logs
import  logging,time
import sys,io,os
class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.start=sys.stdout
        self.fp = fp

    def write(self, s):
        self.fp.write(s)
        # a=sys.stdout
        self.file = open("text.txt", "a+")
        self.file.write(s)
        self.file.flush()
        sys.stdout = self.start
        print(s)
        # sys.stdout=a


        # self.file.close()
    def writelines(self, lines):
        self.fp.writelines(lines)
    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)
class  A():
    def __init__(self):
        self.stdout0 = None
        self.stderr0 = None
        # self.logger= logging.getLogger(__name__)
        # self.stream = open(r"E:\PyFiles\Besettest\besettest\log\myLog\test.log","ab+")
        self.startTest()
        self.logger = logs(self.__class__.__name__)
    def startTest(self):

        self.outputBuffer=io.StringIO()

        stdout_redirector.fp=self.outputBuffer
        stderr_redirector.fp=self.outputBuffer
        # self.stdout0 = sys.stdout  # 记录标准输出原始位置
        # self.stderr0 = sys.stderr

        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

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



a=A()
a.c()
