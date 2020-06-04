#!/usr/bin/python3
# @File:.py
# -*- coding:utf-8 -*-
# @Author:von_fan
# @Time:2020年06月05日00时30分34秒

import  re,os

class MakeScript(object):
    def __init__(self):
        self.copy=open("../interface/test_all_case.py","r",encoding='utf8')
        self.file=open("../interface/test_all.py","a",encoding='utf8')
    def write(self, s):
        self.file.write(s)

    def read(self):
        return self.copy.readlines()

    def writelines(self, lines):
        self.file.writelines(lines)

    def flush(self):
        self.file.flush()

    def start_write(self):
        pass
if __name__=="__main__":
    files=MakeScript()

    for item in files.read():

        if "TestCase" in item:
            print(item, type(item))
            item=item.replace("class_name_code","test1")
        files.write(item)

        files.flush()


