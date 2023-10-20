## フォルダ構造
```
- project_root/
  |- Dockerfile
  |- docker-compose.yaml
  |- nginx/
  |  |- nginx.conf
  |- src/
  |  |- manage.py
  |  |- ...
```

## デプロイ手順
1. GitHubからソースコードをクローン及びフォルダ名をsrcに変更
```
git clone your_github_repo_url src
```

2. Dockerコンテナをビルドと起動
```
docker-compose up --build -d
```

アプリケーションは http://localhost/ でアクセス可能
phpMyAdminは http://localhost:8080/ でアクセス可能

## MySQLの設定方法
1. Djangoの設定ファイル（`settings.py`）を開き、データベースの設定を変更する。

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'o-hara_db',
           'USER': 'admin',
           'PASSWORD': 'o-hara',
           'HOST': 'mysql_db', # dbコンテナ
           'PORT': '3306',
       }
   }
   ```
2. データベースのマイグレーションを行う。
```
docker compose exec web python manage.py migrate
```

## デバッグツールの設定方法
Django Debug Toolbarは、Djangoアプリケーションのデバッグを支援するためのツールです。以下は、Django Debug Toolbarを設定する手順です。

1. django-debug-toolbarをインストールします。
```
pip install django-debug-toolbar
```

2. settings.pyファイルにmimetypeのインポート文を書きます。
```python
import mimetypes
mimetypes.add_type("application/javascript", ".js", True)
```
3. settings.pyファイルにdebug_toolbarアプリケーションを追加します。
```python
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
    # ...
]
```
4. settings.pyファイルのMIDDLEWAREリストに、debug_toolbar.middleware.DebugToolbarMiddlewareを追加します。
```python
MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]
```
5. settings.pyファイルに、INTERNAL_IPSリストを追加します。このリストには、Django Debug Toolbarを表示するIPアドレスを指定します。
```python
INTERNAL_IPS = ['127.0.0.1', '::1', 'localhost', '0.0.0.0']
ROOT_URLCONF = 'testDjango.urls'
```
この設定は、ローカルホストからのアクセスのみを許可するため、セキュリティ上の理由から重要です。
6. settings.pyにNginxのリバースプロキシに対応する設定を行います。
```python
def show_debug_toolbar(request):
    return request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS

DEBUG_TOOLBAR_CALLBACK = show_debug_toolbar

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    'STATIC_URL': '/debug_toolbar/',
}
```
7. urls.pyファイルに、Django Debug ToolbarのURLconfをインポートします。
```python
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
```

## Sassの設定方法
1. VSCodeの拡張でLive Sass Compilerをインストール
2. LiveSassCompilerの設定画面からFormatsをsettings.jsonで開く
3. savePathのディレクトリでcssファイルの出力先を指定する。（ルートは現在開いているディレクトリが基点）
```json
"savePath": "/src/app/static/app/css",
```
4. 画面右下のwatchsassボタンをクリックするとリアルタイムでコンパイルして指定フォルダへ出力される。

## サーバーサイドの編集について
※サーバーを再起動しないと反映されません。
```bash
docker compose restart web
```
3秒かからず再起動が完了し、反映されます。

## フロントエンドの編集について
※nginxに静的ファイルを送らないと反映されません。
1. コンテナ内に入ります。
```bash
docker exec -it django_gunicorn /bin/bash
```
2. collectstaticコマンドでnginxに静的ファイルを送ります。
```bash
python manage.py collectstatic --noinput
```
※即時反映されます。shift + F5でスーパーリロードしてください。