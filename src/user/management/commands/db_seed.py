from django.core.management.base import BaseCommand
from django_seed import Seed
from user.models import CustomUser
from diary.models import Diary, Emotion, Week_AI, Month_AI
from faker import Faker
from django.contrib.auth.hashers import make_password
from allauth.account.models import EmailAddress
import csv

class Command(BaseCommand):
    help = 'Seeds the database with data for myapp'
    fake = Faker('ja_JP')

    def handle(self, *args, **options):
        # サンプルユーザーデータを生成
        seeder = Seed.seeder(locale='ja_JP')
        fake = Faker('ja_JP')
        seeder.add_entity(CustomUser, 10, {
            'email': lambda x: fake.email(),
            'username': lambda x: fake.user_name(),
            'password': make_password('12345678p'),
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        })
        seeder.execute()

        # 生成されたユーザーオブジェクトを取得
        user_objects = CustomUser.objects.all()

        # 生成されたユーザーオブジェクトを利用してEmailAddressを登録
        for user_data in user_objects:
            email_address = EmailAddress.objects.create(
                user=user_data,
                email=user_data.email,
                primary=True,
                verified=True
            )
            email_address.save()
            
        # CSVファイルからDiaryモデルのデータを読み込んでリストに格納
        with open('csv/diary_diary.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            diaries_data_list = [row for row in reader]

        # CSVファイルからEmotionモデルのデータを読み込んでリストに格納
        with open('csv/diary_emotion.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            emotions_data_list = [row for row in reader]

        for user_data in user_objects:
            # 1ユーザー分のデータを取得
            user_diaries_data_list = [
                {**data, 'user_id': user_data.id} for data in diaries_data_list
            ]

            # Diaryモデルに対してのデータをシード
            diaries = Diary.objects.bulk_create([
                Diary(
                    user_id=data['user_id'],
                    content=data['content'],
                    ai_comment=data['ai_comment'],
                    created_date=data['created_date'],
                    updated_date=data['updated_date'],
                    counseling=data['counseling']
                )
                for data in user_diaries_data_list
            ])

            # 生成されたDiaryオブジェクトを利用してEmotionを登録
            emotions_to_create = []
            for data in emotions_data_list:
                diary = Diary.objects.get(user_id=user_data.id, created_date=data['created_date'])
                emotion_data = {
                    'user': user_data,
                    'diary': diary,
                    'reasoning': data['reasoning'],
                    'positive': data['positive'],
                    'negative': data['negative'],
                    'neutral': data['neutral'],
                    'mixed': data['mixed'],
                    'created_date': data['created_date'],
                    'updated_date': data['updated_date'],
                }
                emotions_to_create.append(Emotion(**emotion_data))

            emotions = Emotion.objects.bulk_create(emotions_to_create)
        # CSVファイルからMonth_AIモデルのデータを読み込んでリストに格納
        with open('csv/diary_month_ai.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            month_ais_data_list = [row for row in reader]

        # Month_AIデータをユーザーごとに複製してシード
        for user_data in user_objects:
            # 1ユーザー分のデータを取得
            user_month_ais_data_list = [
                {**data, 'user_id': user_data.id} for data in month_ais_data_list
            ]

            # Month_AIモデルに対してのデータをシード
            month_ais = Month_AI.objects.bulk_create([
                Month_AI(
                    user_id=data['user_id'],
                    ai_comment=data['ai_comment'],
                    created_date=data['created_date'],
                    updated_date=data['updated_date'],
                )
                for data in user_month_ais_data_list
            ])

        # CSVファイルからWeek_AIモデルのデータを読み込んでリストに格納
        with open('csv/diary_week_ai.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            week_ais_data_list = [row for row in reader]

        # Week_AIデータをユーザーごとに複製してシード
        for user_data in user_objects:
            # 1ユーザー分のデータを取得
            user_week_ais_data_list = [
                {**data, 'user_id': user_data.id} for data in week_ais_data_list
            ]

            # Week_AIモデルに対してのデータをシード
            week_ais = Week_AI.objects.bulk_create([
                Week_AI(
                    user_id=data['user_id'],
                    ai_comment=data['ai_comment'],
                    created_date=data['created_date'],
                    updated_date=data['updated_date'],
                )
                for data in user_week_ais_data_list
            ])

        self.stdout.write(self.style.SUCCESS('データベースの接続に成功しました'))
