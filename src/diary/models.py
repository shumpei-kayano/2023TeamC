from django.db import models
from user.models import CustomUser

class Diary(models.Model):
    '''日記モデル'''

    # ユーザーへの外部キー
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    # 日記の内容
    content = models.TextField(verbose_name='内容', max_length=1050, blank=False, null=False)
    # 作成日時
    created_date = models.DateField(verbose_name='作成日時', null=True)
    # 更新日時
    updated_date = models.DateField(verbose_name='更新日時', auto_now=True,null=True)
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
    # カウンセリング可否
    counseling = models.IntegerField(verbose_name='カウンセリング可否', default=0)

    def __str__(self):
        return f'Diary by {self.user}'

class Month_AI(models.Model):
    '''月の総評モデル'''

    # ユーザーへの外部キー
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    # AIコメント
    ai_comment = models.CharField(verbose_name='AIコメント', max_length=1000)
    # 作成日時
    created_date = models.DateField(verbose_name='作成日時')
    # 更新日時
    updated_date = models.DateField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return f'Diary by {self.user}'

class Week_AI(models.Model):
    '''週の総評モデル'''

    # ユーザーへの外部キー
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    # AIコメント
    ai_comment = models.CharField(verbose_name='AIコメント', max_length=1000)
    # 作成日時
    created_date = models.DateField(verbose_name='作成日時')
    # 更新日時
    updated_date = models.DateField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return f'Diary by {self.user}'

class Emotion(models.Model):
    '''感情分析モデル'''
    # ユーザーへの外部キー
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
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
    # 作成日時
    created_date = models.DateField(verbose_name='作成日時',null=True)
    # 更新日時
    updated_date = models.DateField(verbose_name='更新日時', auto_now=True)

    def __str__(self):
        return f'Emotion analysis for Diary {self.diary}'
      
    @property
    def month_day(self):
      return f"{self.created_date.month}月{self.created_date.day}日"
