

class class_name_code(unittest.TestCase):

    def setUp(self):
        self.__class__.__name__ = "__class_name__"
        self.logger = logs(self.__class__.__name__)

    def tearDown(self):
        pass