import csv

from django.core.management.base import BaseCommand, CommandError

from injures.models import Injure

DATA_DIR = 'data/table_of_injures.csv'


class Command(BaseCommand):

    def batch(self, bulk: list) -> None:
        Injure.objects.bulk_create(bulk)

    def check_exsists_record(self, queryset, name) -> bool:
        return queryset.filter(name=name).exists()

    def handle(self, *args, **options):
        try:
            with open(DATA_DIR, encoding='UTF-8') as csvfile:
                injures = csv.reader(csvfile, dialect='excel')
                queryset = Injure.objects.all()
                bulk = []
                for injure in injures:
                    if not self.check_exsists_record(queryset, injure[0]):
                        data = {
                            'name': injure[0],
                            'description': injure[1],
                            'body_part': injure[2],
                        }
                        bulk.append(Injure(**data))
                self.batch(bulk)
        except Exception as error:
            raise CommandError(error)
        self.stdout.write('Injures was updated')
