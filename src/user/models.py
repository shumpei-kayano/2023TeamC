from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# カスタムユーザーマネージャークラスを定義
class CustomUserManager(BaseUserManager):
    # 一般のユーザーを作成するメソッド
    def create_user(self, username, email, password=None, ):
        # メールアドレスが指定されていない場合はエラーを発生させる
        if not email:
            raise ValueError('The Email field must be set')
        # メールアドレスを正規化（小文字化）する
        email = self.normalize_email(email)
        # ユーザーオブジェクトを作成
        user = self.model(username=username, email=email, )
        # パスワードをハッシュ化してユーザーオブジェクトに設定
        user.set_password(password)
        # ユーザーオブジェクトをデータベースに保存
        user.save(using=self._db)
        # 作成したユーザーオブジェクトを返す
        return user

    # # スーパーユーザーを作成するメソッド
    def create_superuser(self, username, email, password=None, ):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        # create_user メソッドを使用してスーパーユーザーを作成
        return self.create_user(username, email, password, )
# カスタムユーザーモデルを定義/
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # プライマリキーとして id カラムを定義
    # id = models.AutoField(primary_key=True)
    # ユーザー名を格納するフィールド
    username = models.CharField(max_length=30, unique=True)
    # メールアドレスを格納するフィールド
    email = models.EmailField(unique=True)
    # # ユーザーアカウントが有効かどうかを示すフィールド
    is_active = models.BooleanField(default=True)
    # # スタッフ権限を持つかどうかを示すフィールド
    is_staff = models.BooleanField(default=False)
    # CustomUserManager をオブジェクトとして使用
    objects = CustomUserManager()
    # ユーザー名を識別子として使用
    USERNAME_FIELD = 'email'
    # メールアドレスを識別子として使用
    # EMAIL_FIELD = 'email'
    # ユーザー作成時に必須のフィールド（メールアドレス）を指定
    REQUIRED_FIELDS = []
    # ユーザー名を表示用の文字列として設定
    def __str__(self):
        return self.username
