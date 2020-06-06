

class class_name_code(unittest.TestCase):

    def setUp(self):
        self.__class__.__name__ = "__class_name__"
        logger.info("执行前置操作")

    def tearDown(self):
        logger.info("后置操作")