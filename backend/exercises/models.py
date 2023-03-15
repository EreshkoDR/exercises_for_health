from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.settings import MEDIA_ROOT
from injures.models import BodyParts

EXERCISES_ROOT = MEDIA_ROOT / 'exercises'


class BaseExercisesModel(models.Model):
    """Базовая модель для упражнений."""
    # Difficulty
    BEGINNER = 'beginner'
    NORMAL = 'normal'
    HARDCORE = 'hardcore'
    DIFFICULTY_CHOISES = [
        (BEGINNER, _('Beginner')),
        (NORMAL, _('Normal')),
        (HARDCORE, _('Hardcore')),
    ]
    # Type of activity
    POWER = 'power'
    STRETCH = 'stretch'
    MIX = 'mix'
    STATIC = 'static'
    WARM_UP = 'warm_up'
    WARM_DOWN = 'warm_down'
    TYPE_OF_ACTIVITY_CHOISES = [
        (POWER, _('Power')),
        (STRETCH, _('Stretch')),
        (MIX, _('Mix')),
        (STATIC, _('Static')),
        (WARM_UP, _('Warm up')),
        (WARM_DOWN, _('Warm down')),
    ]

    name = models.CharField(
        _('Name of exercise'),
        max_length=150
    )
    body_part = models.CharField(
        _('Part of body'),
        choices=BodyParts.BODY_PARTS_CHOISES,
        max_length=10
    )
    difficulty = models.CharField(
        _('Difficulty of exercise'),
        choices=DIFFICULTY_CHOISES,
        max_length=10
    )
    type_of_activity = models.CharField(
        _('Type of activity'),
        choices=TYPE_OF_ACTIVITY_CHOISES,
        max_length=10,
    )
    description = models.TextField(
        _('Descriptoin of exercise')
    )
    exercise = models.TextField(
        _('Description for doing exercise')
    )
    file = models.FileField(
        upload_to=EXERCISES_ROOT / str(body_part)
    )

    def __str__(self):
        return f'{self.body_part}, {self.name}, {self.type_of_activity}'
