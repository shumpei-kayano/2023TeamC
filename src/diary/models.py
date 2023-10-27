from django.db import models
from user.models import CustomUser

class Diary(models.Model):
    '''日記モデル'''

    # ユーザーへの外部キー
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    # 日記の内容
    content = models.TextField(verbose_name='内容', max_length=1000, blank=False, null=False)
    # 作成日時
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    # 更新日時
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    # 写真へのリンク (空であることも許可)
    photo1 = models.ImageField(verbose_name='写真1', upload_to='diary_photos/', blank=True, null=True)
    photo2 = models.ImageField(verbose_name='写真2', upload_to='diary_photos/', blank=True, null=True)
    photo3 = models.ImageField(verbose_name='写真3', upload_to='diary_photos/', blank=True, null=True)
    photo4 = models.ImageField(verbose_name='写真4', upload_to='diary_photos/', blank=True, null=True)
    # 動画へのリンク (空であることも許可)
    movie1 = models.FileField(verbose_name='動画1', upload_to='diary_movie/', blank=True, null=True)
    movie2 = models.FileField(verbose_name='動画2', upload_to='diary_movie/', blank=True, null=True)
    movie3 = models.FileField(verbose_name='動画3', upload_to='diary_movie/', blank=True, null=True)
    movie4 = models.FileField(verbose_name='動画4', upload_to='diary_movie/', blank=True, null=True)

    # AIコメント
    ai_comment = models.CharField(verbose_name='AIコメント', max_length=1000)

    def __str__(self):
        return f'Diary by {self.user}'

class Emotion(models.Model):
    '''感情分析モデル'''

    # 日記への外部キー
    diary = models.ForeignKey(Diary, verbose_name='日記', on_delete=models.PROTECT)
    # 感情推論
    reasoning = models.CharField(verbose_name='感情推論', max_length=10)
    # ポジティブな感情スコア
    positive = models.FloatField(verbose_name='ポジティブ')
    # ネガティブな感情スコア
    negative = models.FloatField(verbose_name='ネガティブ')
    # 中立な感情スコア
    neutral = models.FloatField(verbose_name='中立')
    # 混合感情スコア
    mixed = models.FloatField(verbose_name='混合')
    # 週番号
    week_number = models.IntegerField(verbose_name='週番号')
    # 月
    month = models.IntegerField(verbose_name='月')
    # 週
    week = models.IntegerField(verbose_name='週')
    # 日
    day = models.IntegerField(verbose_name='日')
    # 年
    year = models.IntegerField(verbose_name='年')

    def __str__(self):
        return f'Emotion analysis for Diary {self.diary}'
