from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

# 画像のURLを追加
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# debug_toolbarの設定
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]