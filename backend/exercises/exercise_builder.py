from random import choices
from typing import List

from backend.settings import EXERCISES_COUNT
from exercises.models import BaseExercisesModel
from injures.models import BodyParts
from users.models import User


class WorkoutProgramm():
    """
    ## Сборщик программы тренировки.
    Принимает модель пользователя и составляет
    разминочную, основную и заключительную часть занятия, собирает и кладёт
    во внутреннюю переменную `__programm`.
    ### functions
    - `get_programm()` - возвращает собранный список моделей упражнений
    -> `List[BaseExercisesModel,]`

    - `get_video()` - возвращает список FieldFile модели упражнений
    -> `List[FieldFile,]`

    - `refresh_programm()` - пересобирает программу
    -> `None`

    ### property
    - `count` - возвращает колличество упражнений в программе занятия
    -> `int`
    """
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
        self.__user: User = user
        self.__bmi: int = user.bmi
        self.__difficulty_set: set = self.get_difficulty()
        self.__injures_set: set = {
            injure.injures.body_part
            for injure in self.__user.personal_injures.all()
        }
        self.__body_parts_set: set = self.__get_set_of_body_parts(
            self.__injures_set
        )
        self.__full_set: set = set.union(
            self.__injures_set,
            self.__body_parts_set
        )
        self.__queryset_exercises = BaseExercisesModel.objects.filter(
            body_part__in=self.__full_set
        )
        self.__programm: list = []
        self.__main()

    def get_difficulty(self) -> set:
        difficulty_dict = {
            BaseExercisesModel.BEGINNER: (
                BaseExercisesModel.BEGINNER
            ),
            BaseExercisesModel.NORMAL: (
                BaseExercisesModel.NORMAL,
                BaseExercisesModel.BEGINNER
            ),
            BaseExercisesModel.HARDCORE: (
                BaseExercisesModel.HARDCORE,
                BaseExercisesModel.NORMAL,
                BaseExercisesModel.BEGINNER
            ),
        }
        return difficulty_dict.get(self.__user.difficulty_level)

    def __get_set_of_body_parts(self, injures_set: set) -> set:
        """
        ### Выборка частей тела / отделов позвоночника
        Функция принимает сет проблемных участков пользователя и возвращает
        близлежащие части / отделы (выше и/или ниже).
        ###### Требуется для соблюдения методологии построения занятия
        """
        result = set()
        invert_dict = {
            str(value): key
            for key, value in BodyParts.MAP_OF_BODY_PARTS.items()
        }
        for injure in injures_set:
            index = BodyParts.MAP_OF_BODY_PARTS[injure]
            match index:
                case 0:
                    result.add(invert_dict[str(index + 1)])
                    # Исключительный случай
                    result.add(BodyParts.SHOULDERS)
                case 5:
                    result.add(invert_dict[str(index - 1)])
                case 7:
                    result.add(invert_dict[str(index + 1)])
                case 9:
                    result.add(invert_dict[str(index - 1)])
                case _:
                    result.add(invert_dict[str(index + 1)])
                    result.add(invert_dict[str(index - 1)])
        return result

    def __get_max_exercises(self, type_of_activity: int, query_len) -> int:
        """
        ### Функция подбора колличества упражнений
        Зависит от уровня сложности пользователя и типа активности.
        """
        level = self.__user.difficulty_level
        match type_of_activity:
            case WorkoutProgramm.WARM_UP:
                result = EXERCISES_COUNT.get(level)[type_of_activity]
            case WorkoutProgramm.MAIN_PART:
                result = EXERCISES_COUNT.get(level)[type_of_activity] / 2
            case WorkoutProgramm.WARM_DOWN:
                result = EXERCISES_COUNT.get(level)[type_of_activity]
        if result > query_len:
            return query_len
        return result

    def get_warm_up_part(self) -> List[BaseExercisesModel]:
        queryset = self.__queryset_exercises.filter(
            type_of_activity__in=WorkoutProgramm.WARM_UP_LIST,
            body_part__in=self.__injures_set
        )
        count = self.__get_max_exercises(
            WorkoutProgramm.WARM_UP,
            queryset.count()
        )
        return choices(queryset, k=count)

    def get_main_part(self) -> List[BaseExercisesModel]:
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
        смотри `get_max_exercises()`
        3. Если колличество упражнений в запросах не равное, выбирается
        наименьший список и на основе его длинны в цикле `for` собирается и
        возвращается итоговый список упражнений, имеющий чередование по типу
        выполняемого действия: `power | static`-`stretch | mix`
        """
        if self.__difficulty_set == BaseExercisesModel.BEGINNER:
            query_filter = self.__body_parts_set
        else:
            query_filter = self.__full_set
        queryset_power = self.__queryset_exercises.filter(
            type_of_activity__in=WorkoutProgramm.MAIN_PART_LIST[:2],
            difficulty__in=self.__difficulty_set,
            body_part__in=query_filter
        )
        queryset_stretch = self.__queryset_exercises.filter(
            type_of_activity__in=WorkoutProgramm.MAIN_PART_LIST[2:],
            difficulty__in=self.__difficulty_set,
            body_part__in=query_filter
        )
        exercises = []
        count = self.__get_max_exercises(
            WorkoutProgramm.MAIN_PART,
            queryset_power.count()
        )
        power = choices(queryset_power, k=int(count))
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

    def get_warm_down(self) -> List[BaseExercisesModel]:
        queryset = self.__queryset_exercises.filter(
            type_of_activity__in=WorkoutProgramm.WARM_DOWN_LIST,
            body_part__in=self.__injures_set
        )
        count = self.__get_max_exercises(
            WorkoutProgramm.WARM_DOWN,
            queryset.count()
        )
        return choices(queryset, k=count)

    def __main(self):
        warm_up = self.get_warm_up_part()
        main_part = self.get_main_part()
        warm_down = self.get_warm_down()
        self.__programm = warm_up + main_part + warm_down

    def get_programm(self) -> List[BaseExercisesModel]:
        return self.__programm

    def refresh_programm(self) -> None:
        self.__main()

    def get_video(self) -> List[BaseExercisesModel.file]:
        return [exercise.file for exercise in self.__programm]

    @property
    def count(self) -> int:
        return self.__programm.count()


# from users.models import User
# from exercises.exercise_builder import WorkoutProgramm
# admin = User.objects.get(pk=1)
# test = WorkoutProgramm(admin)
