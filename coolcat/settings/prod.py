import datetime
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 把apps目录加入python导包路径
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

SECRET_KEY = 'f7b-$j#jwgos7j!zl80vp@t@vk#$_!vg9+i$r%6@!1-tp+rh%('

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '39.107.121.208', 'www.kumao.cool']
# 跨域请求白名单
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'https://www.kumao.cool',
)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # 支持跨域请求
    'rest_framework',
    'users.apps.UsersConfig',
    'blogs.apps.BlogsConfig',
    'operation.apps.OperationConfig',
)

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 支持跨域请求
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'coolcat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'coolcat.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'coolcat',
        'USER': 'moon',
        'PASSWORD': 'identified',
        'HOST': '39.107.121.208',
        'PORT': 3306,
    }
}

# 缓存配置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:foobared@39.107.121.208:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # 静态文件目录

MEDIA_URL = 'image/cover/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media/cover')

STATIC_HTTP = 'https://www.kumao.cool'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # jwt认证
        # 'rest_framework.authentication.BasicAuthentication',  # 基本认证
        'rest_framework.authentication.SessionAuthentication',  # session认证
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',  # 自动生成接口文档
}
# DRF扩展
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),  # jwt有效期
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.utils.jwt_response_payload_handler'  # 获取jwt载荷数据
}

# 发送邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'moonpython@163.com'
EMAIL_HOST_PASSWORD = 'L729123265'
DEFAULT_FROM_EMAIL = '酷猫社区<moonpython@163.com>'

# 日志配置
LOGGING = {
    'version': 1,  # 版本
    'disable_existing_loggers': True,  # 是否禁用已经存在的日志器
    'formatters': {  # 打印的日志格式
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s]'
                      ' [%(levelname)s]- %(message)s'},
        'simple': {
            'format': '%(levelname)s %(module)s %(created)s %(message)s'
        }
    },
    'filters': {
    },
    'handlers': {  # 用来定义具体处理日志的方式（可定义多种）
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level': 'INFO',
            # 日志文件指定为5M，超过5M重新命名，然后写入新的日志文件
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志输出文件地址
            'filename': os.path.join(BASE_DIR, 'logs/coolcat.log'),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/coolcat.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/coolcat.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'sourceDns.webdns.views': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
        'sourceDns.webdns.util': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}
