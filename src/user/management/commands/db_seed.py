from django.core.management.base import BaseCommand
from django_seed import Seed
from user.models import CustomUser
from diary.models import Diary, Emotion
from faker import Faker
from django.contrib.auth.hashers import make_password
from datetime import timedelta, datetime
import random
from allauth.account.models import EmailAddress


class Command(BaseCommand):
    help = 'Seeds the database with data for myapp'
    fake = Faker('ja_JP')

    def handle(self, *args, **options):
        seeder = Seed.seeder(locale='ja_JP')
        fake = Faker('ja_JP')

        # Userモデルに対して10件のデータをシード
        seeder.add_entity(CustomUser, 10, {
            'email': lambda x: fake.email(),
            'username': lambda x: fake.user_name(),
            'password': make_password('12345678p'),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            # 他のフィールドのカスタマイズ
        })

        # 生成されたデータを取得
        seeder.execute()
        user_objects = CustomUser.objects.all()#こいつで取得するオブジェクトを指定しないと

        # 生成されたUserオブジェクトを利用してEmailAddressを登録
        for user_data in user_objects:
            email_address = EmailAddress.objects.create(
                user=user_data,
                email=user_data.email,
                primary=True,
                verified=True  # ユーザーが既に認証済みの場合はTrueに設定
            )
            email_address.save()

        # # Diaryモデルに対して40件のデータをシード
        # diaries = seeder.add_entity(Diary, 40, {
        #     'user': lambda x: random.choice(users),
        #     'content': lambda x: fake.text(),
        #     'created_date': lambda x: datetime.now() - timedelta(days=fake.random_int(min=1, max=40)),
        #     'updated_date': lambda x: datetime.now() - timedelta(days=fake.random_int(min=1, max=40)),
        #     # 他のフィールドのカスタマイズ
        # })
        # seeder.execute()

        # # Emotionモデルに対して40件のデータをシード
        # reasoning_choices = ['positive', 'negative', 'neutral', 'mixed']
        # seeder.add_entity(Emotion, 40, {
        #     'user': lambda x: random.choice(users),
        #     'diary': lambda x: random.choice(diaries),
        #     'reasoning': lambda x: random.choice(reasoning_choices),
        #     'positive': lambda x: fake.random_int(min=0, max=100),
        #     'negative': lambda x: fake.random_int(min=0, max=100),
        #     'neutral': lambda x: fake.random_int(min=0, max=100),
        #     'mixed': lambda x: fake.random_int(min=0, max=100),
        #     # 他のフィールドのカスタマイズ
        # })

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))
