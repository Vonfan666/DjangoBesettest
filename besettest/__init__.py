from __future__ import absolute_import, unicode_literals
import  pymysql

#启动时检测celery文件
__all__ = ['celery_app']
pymysql.install_as_MySQLdb()


#引入celery实例对象
