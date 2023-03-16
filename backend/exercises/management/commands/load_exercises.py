import csv

from django.core.management.base import BaseCommand, CommandError

from exercises.models import BaseExercisesModel

DATA_DIR = 'data/exercises.csv'


class Command(BaseCommand):
    def batch(self, bulk: list) -> None:
        BaseExercisesModel.objects.bulk_create(bulk)

    def check_exsists_record(self, queryset, name) -> bool:
        return queryset.filter(name=name).exists()

    def handle(self, *args, **options):
        try:
            with open(DATA_DIR, encoding='UTF-8') as csvfile:
                exercises = csv.reader(csvfile, dialect='excel')
                queryset = BaseExercisesModel.objects.all()
                bulk = []
                for exercise in exercises:
                    if not self.check_exsists_record(queryset, exercise[0]):
                        data = {
                            'name': exercise[0],
                            'body_part': exercise[1],
                            'difficulty': exercise[2],
                            'type_of_activity': exercise[3],
                            'description': exercise[4],
                            'exercise': exercise[5],
                            'file': exercise[6]
                        }
                        bulk.append(BaseExercisesModel(**data))
                self.batch(bulk)
        except Exception as error:
            raise CommandError(error)
        self.stdout.write('Exercises was updated')
