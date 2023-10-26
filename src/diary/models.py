from django.db import models
from user.models import CustomUser

class Diary(models.Model):
    '''日記モデル'''

    userID=models.ForeignKey(CustomUser,verbose_name='ユーザーID',on_delete=models.PROTECT)
    content=models.TextField(verbose_name='内容', blank=False, null=False)
    create_at=models.DateTimeField(verbose_name='作成日時',auto_now_add=True)
    update_at=models.DateTimeField(verbose_name='更新日時',auto_now_add=True)
    photo=models.CharField(verbose_name='写真')
    movie=models.CharField(verbose_name='動画')
    AI=models.CharField(verbose_name='AIコメント')

    def __str__(self):
        return self.userID

class emotion(models.Model):
    '''感情分析モデル'''

    DiaryID=models.ForeignKey(Diary,verbose_name='日記ID',on_delete=models.PROTECT)
    Reasoning=models.CharField(verbose_name='感情推論')
    positive=models.FloatField(verbose_name='ポジティブ')
    negative=models.FloatField(verbose_name='ネガティブ')
    normal=models.FloatField(verbose_name='中立')
    mixing=models.FloatField(verbose_name='混合')
    weeknum=models.IntegerField(verbose_name='週番号')
    month=models.IntegerField(verbose_name='月')
    week=models.IntegerField(verbose_name='週')
    day=models.IntegerField(verbose_name='日')
    year=models.IntegerField(verbose_name='年')

    def __str__(self):
        return self.DiaryID
