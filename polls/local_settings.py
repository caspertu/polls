#!/usr/bin/env python
# coding: utf-8
# casper@2013/05/27

import os

# 时区
TIME_ZONE = 'Asia/Shanghai'

# 语言
LANGUAGE_CODE = 'zh-cn'

# 邮箱（报错时发送）
EMAIL = 'caspertu@gmail.com'

# 数据库信息
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # mysql 可以改成 'postgresql_psycopg2', 'postgresql', 'sqlite3' or 'oracle'.
        'NAME': 'sqlite.dat',                      # 数据库名
        'USER': '',                      # sqlite3 不使用此配置
        'PASSWORD': '',                  # sqlite3 不使用此配置
        'HOST': '',
        'PORT': '',
    }
}

# email config
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'caspertu@gmail.com'  
EMAIL_HOST_PASSWORD = 'Tian1ocs'
