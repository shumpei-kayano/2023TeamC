from pathlib import Path
import os
# debug_toolbarの設定
import mimetypes
mimetypes.add_type("application/javascript", ".js", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^kcmqusi%2#6(yl+c3f(7d36c10ak$)2f9)-)qa0nu*@^41pm@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'debug_toolbar',
    'sass_processor',
    'user',
    'diary',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

AUTH_USER_MODEL = 'user.CustomUser' # 追加

#django-allauthで利用するdjango.contrib.sitesを使うためにサイト識別用IDを設定
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
  #一般ユーザー用（メールアドレス認証）
  'allauth.account.auth_backends.AuthenticationBackend',
  #管理サイト用（ユーザー名認証）
  'django.contrib.auth.backends.ModelBackend',
)
# settings.py

# メールによる認証を使用
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False

#サインアップにメールアドレス確認をはさむように設定
ACCOUNT_EMAIL_VERIFICATION= 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

#ログイン/ログアウト後の遷移先を設定
LOGIN_REDIRECT_URL = 'diary:home_top'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'

#ログアウトリンクのクリック一発でログアウトする設定
# ACCOUNT_LOGOUT_ON_GET =True

#django-allauthが送信するメールの件名に自動付与される接頭語をブランクに設定
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''

#デフォルトのメール送信元を設定
DEFAULT_FROM_EMAIL = os.environ.get('FROM_EMAIL')

# settings.py

# Allauthのメール確認を無効にする
ACCOUNT_EMAIL_VERIFICATION = 'none'




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

INTERNAL_IPS = ['127.0.0.1', '::1', 'localhost', '0.0.0.0']

ROOT_URLCONF = 'TeamC.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.normpath(os.path.join(BASE_DIR, 'user/templates/')),
        ],
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

WSGI_APPLICATION = 'TeamC.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'o-hara_db',
        'USER': 'admin',
        'PASSWORD': 'o-hara',
        'HOST': 'mysql_db', # dbのコンテナ名
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/usr/share/nginx/html/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 画像ファイルのアップロード先
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

def show_debug_toolbar(request):
    return request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS

DEBUG_TOOLBAR_CALLBACK = show_debug_toolbar

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    'STATIC_URL': '/debug_toolbar/',
}