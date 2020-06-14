
    def test_method_name(self):
        self.__dict__["_testMethodName"] = "__method_name__"
        data={}
        res=s.action(data,self.logger)
