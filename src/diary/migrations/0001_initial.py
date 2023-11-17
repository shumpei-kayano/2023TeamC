# Generated by Django 4.2 on 2023-10-27 02:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000, verbose_name='内容')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='作成日')),
                ('updated_date', models.DateField(auto_now=True, verbose_name='更新日')),
                ('photo1', models.ImageField(blank=True, null=True, upload_to='diary_photos/', verbose_name='写真1')),
                ('photo2', models.ImageField(blank=True, null=True, upload_to='diary_photos/', verbose_name='写真2')),
                ('photo3', models.ImageField(blank=True, null=True, upload_to='diary_photos/', verbose_name='写真3')),
                ('photo4', models.ImageField(blank=True, null=True, upload_to='diary_photos/', verbose_name='写真4')),
                ('movie1', models.FileField(blank=True, null=True, upload_to='diary_movie/', verbose_name='動画1')),
                ('movie2', models.FileField(blank=True, null=True, upload_to='diary_movie/', verbose_name='動画2')),
                ('movie3', models.FileField(blank=True, null=True, upload_to='diary_movie/', verbose_name='動画3')),
                ('movie4', models.FileField(blank=True, null=True, upload_to='diary_movie/', verbose_name='動画4')),
                ('ai_comment', models.CharField(max_length=1000, verbose_name='AIコメント')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reasoning', models.CharField(max_length=10, verbose_name='感情推論')),
                ('positive', models.FloatField(verbose_name='ポジティブ')),
                ('negative', models.FloatField(verbose_name='ネガティブ')),
                ('neutral', models.FloatField(verbose_name='中立')),
                ('mixed', models.FloatField(verbose_name='混合')),
                ('week_number', models.IntegerField(verbose_name='週番号')),
                ('month', models.IntegerField(verbose_name='月')),
                ('day', models.IntegerField(verbose_name='日')),
                ('year', models.IntegerField(verbose_name='年')),
                ('diary', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='diary.diary', verbose_name='日記')),
            ],
        ),
    ]
