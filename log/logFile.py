import  logging,os,time



def logger(name):
    logger=logging.getLogger(os.path.basename(name))
    print(os.path.split(os.path.abspath(__file__))[0])
    consoleLog=logging.StreamHandler()
    fileLog=logging.FileHandler(os.path.split(os.path.abspath(__file__))[0]+"\\logs\\test.log")



    logger.addHandler(consoleLog)
    logger.addHandler(fileLog)

    fmt=logging.Formatter('[%(asctime)s](%(levelname)s)%(name)s : %(message)s')  #日志打印格式

    consoleLog.setFormatter(fmt)
    fileLog.setFormatter(fmt)
    # logger.removeHandler(formartter)#控制台重复去掉一
    logger.setLevel('INFO')
    print(os.path.abspath(__file__))
    print(os.path.split(os.path.abspath(__file__))[0]+"\\logs\\test.log")
    return logger


if __name__=="__main__":

    logger=logger(__file__)
    logger.info('hehe')
    logger.warning('haha1')
