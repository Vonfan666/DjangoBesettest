from __future__ import absolute_import
import os
from celery import Celery
# from  besettest.settings import TIME_ZONE
# from django.utils import timezone

# 只要是想在自己的脚本中访问Django的数据库等文件就必须配置Django的环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'besettest.settings')

# app名字
app = Celery('besettest')

# 配置celery
class Config:
    BROKER_URL = 'redis://localhost:6379/2'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/3'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'# 任务序列化方式
    CELERY_RESULT_SERIALIZER = 'json'# 任务结果序列化方式
    CELERY_ENABLE_UTC = False  # 关闭时区
    CELERY_TIMEZONE = 'Asia/Shanghai' # 设置 django-celery-beat 真正使用的时区
    DJANGO_CELERY_BEAT_TZ_AWARE = False # 使用 timezone naive 模式，不存储时区信息，只存储经过时区转换后的时间

    CELERY_TASK_RESULT_EXPIRES =  60 * 60 * 24  # 超过时间
    CELERY_MESSAGE_COMPRESSION = 'zlib'  # 是否压缩
    CELERYD_CONCURRENCY = 4  # 并发数默认已CPU数量定
    CELERYD_PREFETCH_MULTIPLIER = 4  # celery worker 每次去redis取任务的数量
    CELERYD_MAX_TASKS_PER_CHILD = 3  # 每个worker最多执行3个任务就摧毁，避免内存泄漏
    CELERYD_FORCE_EXECV = True  # 可以防止死锁

    CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'  # 配置 celery 定时任务使用的调度器，使用django_celery_beat插件用来动态配置任务

    # CELERY_DISABLE_RATE_LIMITS = True # 禁用所有速度限制，如果网络资源有限，不建议开足马力。
app.config_from_object(Config)

# 到各个APP里自动发现tasks.py文件
app.autodiscover_tasks(
    ["case"],
)
