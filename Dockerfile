FROM python:3.11

RUN apt-get update && apt-get install -y nodejs npm

# プロジェクト名を変更すること（testDjangoの部分）
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE TeamC.settings

# Set the working directory in the container
WORKDIR /app

# 依存関係をインストール
COPY requirements.txt /app/
RUN pip install pip --upgrade
RUN pip install --no-cache-dir -r requirements.txt

# srcディレクトリをコンテナにコピー
COPY ./src /app

# Gunicornの起動 プロジェクト名を変更すること（testDjangoの部分）
CMD ["gunicorn", "TeamC.wsgi:application", "--bind", "0.0.0.0:8000"]
