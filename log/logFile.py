import  logging,os,time



def logger(file):
    logger=logging.getLogger(os.path.basename(file))
    print(os.path.split(os.path.abspath(__file__))[0])
    consoleLog=logging.StreamHandler()
    fileLog=logging.FileHandler(os.path.split(os.path.abspath(__file__))[0]+"\\myLog\\test.log")
    if not logger.handlers:
        logger.addHandler(consoleLog)
        logger.addHandler(fileLog)

        fmt=logging.Formatter('[%(asctime)s](%(levelname)s)%(name)s-%(lineno)d : %(message)s')  #日志打印格式

        consoleLog.setFormatter(fmt)
        fileLog.setFormatter(fmt)
        # logger.removeHandler(consoleLog)#控制台重复去掉一
        # logger.removeFilter(fileLog) #日志文件去掉重复
        logger.setLevel('INFO')

    return logger


if __name__=="__main__":

    logger=logger(__name__)
    logger.info('hehe')
    logger.warning('haha1')
    print(os.path.split(os.path.abspath(__file__)))