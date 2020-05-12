"""
Django settings for besettest project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os,sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR) #将根目录临时添加到环境变量
sys.path.insert(0,os.path.join(BASE_DIR,"apps")) #将Mx_Shop/apps临时添加到环境变量
sys.path.insert(0,os.path.join(BASE_DIR,"extra_apps")) #将Mx_Shop/apps临时添加到环境变量

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hnr7eed9rkpd7iqa7l#8a(^pt0w4$^7jd-7k#!9=zzrel)c-pv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*",]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "users",    #因为apps已经设置为根目录 所以可以直接找到users
    "project",
    "rest_framework",
    "django_filters",
    'rest_framework.authtoken',    #token验证

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

WSGI_APPLICATION = 'besettest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "besettest",
        'USER':"root",
        "PASSWORD":"123456",
        "HOST":"LOCALHOST",
        "PORT":"3306",
        "OPTIONS":{"init_command":"SET default_storage_engine=INNODB;"},
        "init_command":"SET foreign_key_checks = 0;", #取消外检检查
        'TEST': {
    'CHARSET' : 'utf8',
    'COLLATION':'utf8_general_ci'

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

LANGUAGE_CODE = 'zh-hans'   #其中 zh-Hans是简体中文  zh-Hant是繁体中文

TIME_ZONE = 'Asia/Shanghai'  #上海时间

USE_I18N = True   #国际化支持 I18N

USE_L10N = True

USE_TZ = False   #USE_TZ设置为True,Django会使用系统默认设置的时区即America/Chicago,此时的TIME_ZONE不管有没有设置都不起作用。


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': (
        # 认证用户可以操作
        'rest_framework.permissions.IsAuthenticated', #设置认证权限
         # 'rest_framework.permissions.IsAdminUser',  #仅管理员用户
        # 所有用户可以操作
        # 'rest_framework.permissions.AllowAny',
        # 认证的用户可以完全操作，否则只能get读取
       # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # 上面两个用于DRF基本验证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  #完成token验证并返回user和token
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',  # djangorestframework_simplejwt JWT认证
    ),

    "DEFAULT_SCHEMA_CLASS":"rest_framework.schemas.AutoSchema", #接口文档docs配置
    # 'NON_FIELD_ERRORS_KEY': 'error', #修改错误信息key
    'EXCEPTION_HANDLER':"libs.exception.custom_exception_handler",
    # 'DEFAULT_RENDERER_CLASSES':('libs.exception.customrenderer',)

}


import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),  #有效期为7天
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    #登录成功自定义返回函数
    'JWT_RESPONSE_PAYLOAD_HANDLER':'libs.authClass.jwt_success_response',
    #登录失败自定义返回函数--这里需要修改源码
    'JWT_RESPONSE_PAYLOAD_ERROR_HANDLER':'libs.authClass.jwt_error_response',
}
AUTHENTICATION_BACKENDS = (
    'libs.authClass.CustomBackend',
)

AUTH_USER_MODEL = 'users.UserProfile'   #路径


MEDIA_URL='/images/'

# LOGOUT_URL = '/users/logout/'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}