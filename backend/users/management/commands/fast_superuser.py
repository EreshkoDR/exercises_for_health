from datetime import datetime

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Fast create superuser admin:admin'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            user = User(username='admin')
            user.set_password('admin')
            user.is_superuser = True
            user.is_staff = True
            user.birthday = datetime(1997, 9, 19)
            user.weight = 72
            user.height = 176
            user.sex = 'male'
            user.save()
            self.stdout.write(self.style.SUCCESS('user admin was created'))
        else:
            self.stdout.write(self.style.WARNING('admin is alredy exists'))
