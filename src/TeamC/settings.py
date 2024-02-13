from pathlib import Path
import os
from dotenv import load_dotenv
# debug_toolbarの設定
import mimetypes
import datetime

# .envファイルを読み込む
load_dotenv()

mimetypes.add_type("application/javascript", ".js", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^kcmqusi%2#6(yl+c3f(7d36c10ak$)2f9)-)qa0nu*@^41pm@'

# デバック
DEBUG = False

# 本番環境だと変える
ALLOWED_HOSTS = ['34.233.79.231','52.201.75.237','teamc.o-hara-oita.click','teamc-sub.o-hara-oita.click', 'localhost']





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
    'axes',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'allauth.account.middleware.AccountMiddleware',#追加
    'axes.middleware.AxesMiddleware',#追加
]

INTERNAL_IPS = ['127.0.0.1', '::1', 'localhost', '0.0.0.0']

ROOT_URLCONF = 'TeamC.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.normpath(os.path.join(BASE_DIR, 'user/templates/account')),
            os.path.normpath(os.path.join(BASE_DIR, 'diary/templates/diary')),
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
        # envからHOSTを読み込む
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'), # RDS作成時のパスワード
        'HOST': os.getenv('DB_HOST'), 
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
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



#---------------------メール送信設定-------------------------
# 以下はSMTPサーバーの設定
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ryougaharada@gmail.com'
EMAIL_HOST_PASSWORD = 'ssnc deay womq kvaf'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Fugoo Customer Support <noreply@example.com>'

# ---------------------メール送信設定-------------------------

# --------------------allauthの基本設定--------------------
# allauthのモデルじゃなくて独自のカスタムユーザーがログイン認証になる
AUTH_USER_MODEL = 'user.CustomUser' 
#django-allauthで利用するdjango.contrib.sitesを使うためにサイト識別用IDを設定
SITE_ID = 1
AUTHENTICATION_BACKENDS = (
  #一般ユーザー用（メールアドレス認証）
  'allauth.account.auth_backends.AuthenticationBackend',
  #管理サイト用（ユーザー名認証）
  'django.contrib.auth.backends.ModelBackend',
)
# メールによる認証を使用
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = True
#サインアップにメールアドレス確認をはさむように設定
ACCOUNT_EMAIL_VERIFICATION= 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
#ログイン/ログアウト後の遷移先を設定
LOGIN_REDIRECT_URL = 'diary:home_top1'
ACCOUNT_LOGOUT_REDIRECT_URL = 'user:account_top'
#ログアウトリンクのクリック一発でログアウトする設定
ACCOUNT_LOGOUT_ON_GET =True
#django-allauthが送信するメールの件名に自動付与される接頭語をブランクに設定
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''

SOCIALACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm'
}

#--------------------allauthの基本設定--------------------

# APIキーの読み込み
# def read_api_key():
#     with open('api_key.txt', 'r') as file:
#         return file.read().strip()

OPENAI_API_KEY = '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'

#--------------------アカウントロック設定--------------------
AXES_FAILURE_LIMIT = 5  # 5回の失敗後にロックアウト

AXES_COOLOFF_TIME = datetime.timedelta(seconds=30) # 30秒間ロック

ACCOUNT_LOCKED_URL = '/accounts/login/'

AXES_LOCKOUT_TEMPLATE ='user/accounts/login/'

AWS_ACCESS_KEY_ID = 'AKIA3VIVOLKQTWBJ5RPH'
AWS_SECRET_ACCESS_KEY = '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'

SESSION_COOKIE_SECURE = True 
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    'https://*.o-hara-oita.click',
]

# settings.py

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'my_session_cookie'