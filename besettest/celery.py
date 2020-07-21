from __future__ import absolute_import
import os
from celery import Celery
from  besettest.settings import TIME_ZONE
# 只要是想在自己的脚本中访问Django的数据库等文件就必须配置Django的环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'besettest.settings')

# app名字
app = Celery('besettest')

# 配置celery
class Config:
    BROKER_URL = 'redis://localhost:6379/2'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/3'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE

app.config_from_object(Config)
# 到各个APP里自动发现tasks.py文件
app.autodiscover_tasks()