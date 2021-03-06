"""
Django settings for besettest project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from __future__ import absolute_import

import os, sys
import logging
import django.utils.log
import logging.handlers
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)  # 将根目录临时添加到环境变量
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))  # 将Mx_Shop/apps临时添加到环境变量
sys.path.insert(0, os.path.join(BASE_DIR, "extra_apps"))  # 将Mx_Shop/apps临时添加到环境变量




redisHost="127.0.0.1:6379"



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hnr7eed9rkpd7iqa7l#8a(^pt0w4$^7jd-7k#!9=zzrel)c-pv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*", ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "users",  # 因为apps已经设置为根目录 所以可以直接找到users
    "project",
    "case",
    "rest_framework",
    "django_filters",
    'rest_framework.authtoken',  # token验证
    # 'django.contrib.staticfiles',
    'channels',
    'django_celery_beat', # 用于动态添加定时任务

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'besettest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# 指定WSGI的路由地址
WSGI_APPLICATION = 'besettest.wsgi.application'
# 指定ASGI的路由地址
ASGI_APPLICATION = 'besettest.routing.application'


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://%s/0'%redisHost,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {  #最大连接数
                'max_connections': 1000
            },
            # 'PASSWORD': 'xxx', # 如果有设置了redis-server密码在这里设置
        }
    },
    'log': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': 'redis://%s/1/log'%redisHost,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {  #最大连接数
                    'max_connections': 1000
                },
                # 'PASSWORD': 'xxx', # 如果有设置了redis-server密码在这里设置
            }
        },
    # 'celery': {
    #             'BACKEND': 'django_redis.cache.RedisCache',
    #             'LOCATION': 'redis://127.0.0.1:6379/2/log',
    #             'OPTIONS': {
    #                 'CLIENT_CLASS': 'django_redis.client.DefaultClient',
    #                 'CONNECTION_POOL_KWARGS': {  #最大连接数
    #                     'max_connections': 1000
    #                 },
    #                 # 'PASSWORD': 'xxx', # 如果有设置了redis-server密码在这里设置
    #             }
    #         }

}


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "besettest",
        'USER': "root",
        "PASSWORD": "123456",
        "HOST": "LOCALHOST",
        "PORT": "3306",
        "OPTIONS": {"init_command": "SET default_storage_engine=INNODB;"},
        "init_command": "SET foreign_key_checks = 0;",  # 取消外检检查
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci'

        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'  # 其中 zh-Hans是简体中文  zh-Hant是繁体中文

TIME_ZONE = 'Asia/Shanghai'  # 上海时间

USE_I18N = True  # 国际化支持 I18N

USE_L10N = True

USE_TZ = False  # USE_TZ设置为True,Django会使用系统默认设置的时区即America/Chicago,此时的TIME_ZONE不管有没有设置都不起作用。
# CELERY_ENABLE_UTC = False
# DJANGO_CELERY_BEAT_TZ_AWARE = False
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': (
        # 认证用户可以操作
        'rest_framework.permissions.IsAuthenticated',  # 设置认证权限
        # 'rest_framework.permissions.IsAdminUser',  #仅管理员用户
        # 所有用户可以操作
        # 'rest_framework.permissions.AllowAny',
        # 认证的用户可以完全操作，否则只能get读取
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',  # 上面两个用于DRF基本验证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # 完成token验证并返回user和token
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',  # djangorestframework_simplejwt JWT认证
    ),

    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.AutoSchema",  # 接口文档docs配置
    # 'NON_FIELD_ERRORS_KEY': 'error', #修改错误信息key
    'EXCEPTION_HANDLER': "libs.exception.custom_exception_handler",
    # 'DEFAULT_RENDERER_CLASSES':('libs.exception.customrenderer',)

}

import datetime

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),  # 有效期为7天
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    # 登录成功自定义返回函数
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'libs.authClass.jwt_success_response',
    # 登录失败自定义返回函数--这里需要修改源码
    'JWT_RESPONSE_PAYLOAD_ERROR_HANDLER': 'libs.authClass.jwt_error_response',
}
AUTHENTICATION_BACKENDS = (
    'libs.authClass.CustomBackend',
)

AUTH_USER_MODEL = 'users.UserProfile'  # 路径

MEDIA_URL = '/images/'

# LOGOUT_URL = '/users/logout/'




LOGGING = {

    'version': 1,
    'disable_existing_loggers': True,  # 禁用所有已经存在的日志配置
    "formatters": {  # 格式器
        'verbose': {  # 详细
            'format': '[%(asctime)s](%(levelname)s)(%(module)s)(%(funcName)s) : %(message)s '
        },
        'simple': {  # 简单
            'format': '[%(asctime)s](%(levelname)s): %(message)s '
        },

    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 处理器，在这里定义了三个处理器

        'console': {  #打印到控制台
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            # "filename": os.path.join(BASE_DIR, "log", "sysLogs", "test.log"),
            # 'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
            # 'backupCount': 3,  # 最多备份几个
            # 'encoding': 'utf-8',
        },

        "requests": {  # 存到文件
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(BASE_DIR, "log", "sysLogs", "test.log"),
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
            'backupCount': 10,  # 最多备份几个
            'encoding': 'utf-8',
        },
        "myLog": {  # 存到文件
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(BASE_DIR, "log", "logs", "test.log"),
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
            'backupCount': 10,  # 最多备份几个
            'encoding': 'utf-8',
        },
        "files": { #存到文件
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(BASE_DIR, "log", "allLogs", "test.log"),
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
            'backupCount': 10,  # 最多备份几个
            'encoding': 'utf-8',

        },
        # 'default': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
        #     'filename': os.path.join(BASE_DIR, "log", "sysLogs", "test.log"),  # 日志文件
        #     'maxBytes': 1024 * 1024 * 5,  # 日志大小 50M
        #     'backupCount': 3,  # 最多备份几个
        #     'formatter': 'verbose',
        #
        # },


        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(BASE_DIR, "log", "sysLogs", "test_errors.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },

    },

    'loggers': {
        "":{   #记录所有日志
            'handlers': ["files"],
            'propagate': True,
            'level': 'DEBUG',
            # 'formatter': 'verbose'
        },
        "django.db.backends":{   #记录所有日志
            'handlers': ["requests","console"],
            'propagate': False,
            'level': 'DEBUG',
            # 'formatter': 'verbose'
        },
         'django.request': {  #记录系统日志
            'handlers': ["error","console"],
            'level': 'ERROR',
            'propagate': False,  # 是否继承父类的log信息
            # 'formatter': 'simple'
        },  # handlers 来自于上面的 handlers 定义的内容
         "log":{   #记录我的日志
            'handlers': ["myLog","console"],
            'propagate': False,
            'level': 'INFO',
            # 'formatter': 'verbose'
        },


    }
}


# # from .celeryCon import *
# #celery配置信息
# #celery中间人 redis://:redis密码@redis服务所在的ip地址:端口/数据库号
# #channels配置redis也是这样配置，如果没有密码，就可以把':redis密码@'省略
# # BROKER_BACKEND = 'redis'
# BROKER_URL = 'redis://localhost:6379/2'
# #celery结果返回，可用于跟踪结果
# CELERY_RESULT_BACKEND ='redis://localhost:6379/3'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE =TIME_ZONE