from typing import List

from backend.settings import EXERCISES_COUNT, MAP_OF_BODY_PARTS
from users.models import User
from random import choices

from exercises.models import BaseExercisesModel


class WorkoutProgramm():
    WARM_UP_LIST = (BaseExercisesModel.WARM_UP,)
    MAIN_PART_LIST = [
        BaseExercisesModel.POWER,
        BaseExercisesModel.STATIC,
        BaseExercisesModel.MIX,
        BaseExercisesModel.STRETCH,
    ]
    WARM_DOWN_LIST = (BaseExercisesModel.WARM_DOWN,)
    WARM_UP = 0
    MAIN_PART = 1
    WARM_DOWN = 2

    def __init__(self, user: User):
        self.user: User = user
        self.bmi = user.bmi
        self.difficulty = self.get_difficulty()
        self.injures_set = {
            injure.injures.body_part
            for injure in self.user.personal_injures.all()
        }
        self.body_parts_set: set = self.get_set_of_body_parts(self.injures_set)
        self.full_set = set.union(self.injures_set, self.body_parts_set)
        self.queryset_exercises = BaseExercisesModel.objects.filter(
            body_part__in=self.full_set
        )
        self.programm = []
        self.__main()

    def get_difficulty(self) -> set:
        difficulty_dict = {
            'beginner': ('beginer'),
            'normal': ('beginner', 'normal'),
            'hardcore': ('beginner', 'normal', 'hardcore'),
        }
        return difficulty_dict.get(self.user.difficulty_level)

    def get_set_of_body_parts(self, injures) -> set:
        result = set()
        invert_dict = {
            str(value): key
            for key, value in MAP_OF_BODY_PARTS.items()
        }
        for injure in injures:
            index = MAP_OF_BODY_PARTS[injure]
            match index:
                case 0:
                    result.add(invert_dict[str(index + 1)])
                case 5:
                    result.add(invert_dict[str(index - 1)])
                case _:
                    result.add(invert_dict[str(index + 1)])
                    result.add(invert_dict[str(index - 1)])
        return result

    def get_max_exercises(self, type_of_activity: int) -> int:
        level = self.user.difficulty_level
        match type_of_activity:
            case WorkoutProgramm.WARM_UP:
                return EXERCISES_COUNT.get(level)[type_of_activity]
            case WorkoutProgramm.MAIN_PART:
                return EXERCISES_COUNT.get(level)[type_of_activity]
            case WorkoutProgramm.WARM_DOWN:
                return EXERCISES_COUNT.get(level)[type_of_activity]
        return 1

    def warm_up(self) -> List[BaseExercisesModel]:
        queryset = self.queryset_exercises.filter(
            type_of_activity__in=WorkoutProgramm.WARM_UP_LIST,
            body_part__in=self.injures_set
        )
        count = self.get_max_exercises(WorkoutProgramm.WARM_UP)
        if count > queryset.count():
            count = queryset.count()
        return choices(queryset, k=count)

    def main_part(self) -> List[BaseExercisesModel]:
        """
        ### Функция сбора основной части занятия.
        0. Настройка фильтра по упражнениям. При `beginner` выбираются только
        те упражнения, которые взаимодействуют с мышцами выше/ниже больного
        участка.
        1. Выполняется два запроса к бд упражнений, с фильтрами по сложности,
        типу активности и частями тела, с которыми необходимо
        взаимодействовать.
        2. Из результатов запросов выбираются `k / 2` случайных упражнений из
        кажного списка.
        `k = (колличество упражнений в выбранной сложности) / 2`.
        3. Если колличество упражнений в запросах не равное, выбирается
        наименьший список и на основе его длинны в цикле `for` собирается и
        возвращается итоговый список упражнений, имеющий чередование по типу
        выполняемого действия: `power`-`stretch`-`power`...`stretch`
        """
        if self.difficulty == 'beginner':
            query_filter = self.body_parts_set
        else:
            query_filter = self.full_set
        queryset_power = self.queryset_exercises.filter(
            type_of_activity__in=WorkoutProgramm.MAIN_PART_LIST[:2],
            difficulty__in=self.difficulty,
            body_part__in=query_filter
        )
        queryset_stretch = self.queryset_exercises.filter(
            type_of_activity__in=WorkoutProgramm.MAIN_PART_LIST[2:],
            difficulty__in=self.difficulty,
            body_part__in=query_filter
        )
        exercises = []
        count = self.get_max_exercises(WorkoutProgramm.MAIN_PART) / 2
        if count > queryset_power.count():
            count = queryset_power.count()
        power = choices(queryset_power, k=int(count))
        if count > queryset_stretch.count():
            count = queryset_stretch.count()
        stretch = choices(queryset_stretch, k=int(count))
        if len(stretch) > len(power):
            lenght = len(power)
        elif len(power) > len(stretch):
            lenght = len(stretch)
        else:
            lenght = len(power)
        for i in range(lenght):
            exercises.append(power[i])
            exercises.append(stretch[i])
        return exercises

    def warm_down(self) -> List[BaseExercisesModel]:
        queryset = self.queryset_exercises.filter(
            type_of_activity__in=WorkoutProgramm.WARM_DOWN_LIST,
            body_part__in=self.injures_set
        )
        count = self.get_max_exercises(WorkoutProgramm.WARM_DOWN)
        if count > queryset.count():
            count = queryset.count()
        return choices(queryset, k=count)

    def get_programm(self) -> List[BaseExercisesModel]:
        return self.programm

    def get_video_list(self) -> list:
        return [exercise.file for exercise in self.programm]

    def refresh_exercises(self) -> None:
        self.__main()

    def __main(self):
        warm_up = self.warm_up()
        main_part = self.main_part()
        warm_down = self.warm_down()
        self.programm = warm_up + main_part + warm_down


# from users.models import User
# from exercises.exercise_builder import WorkoutProgramm
# admin = User.objects.get(pk=1)
# test = WorkoutProgramm(admin)
