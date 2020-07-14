from __future__ import absolute_import, unicode_literals

# 告诉Django在启动时别忘了检测我的celery文件
from .celery import app as celery_ap
import  pymysql
__all__ = ['celery_app']
#启动时检测celery文件
pymysql.install_as_MySQLdb()


#引入celery实例对象
