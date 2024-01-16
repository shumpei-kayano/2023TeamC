from django.core.management.base import BaseCommand
from django_seed import Seed
from user.models import CustomUser  
from faker import Faker
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Seeds the database with data for myapp'
    fake = Faker('ja-JP')
    
    def handle(self, *args, **options):
        seeder = Seed.seeder(locale='ja_JP')

        # Userモデルに対して10件のデータをシード
        seeder.add_entity(CustomUser, 10, {
            'email': lambda x: seeder.faker.email(),
            'username': lambda x: seeder.faker.user_name(),
            'password': make_password('12345678p'),
            'is_active': True,
            'is_staff': False,
            # 他のフィールドのカスタマイズ
        })

        seeder.execute()
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database'))
