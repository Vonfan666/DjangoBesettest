from __future__ import absolute_import, unicode_literals

from besettest.celery import app as celery_app

__all__ = ['celery_app']
import  pymysql
pymysql.install_as_MySQLdb()


