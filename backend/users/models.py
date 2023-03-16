from datetime import datetime, timedelta
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    sex = models.CharField(
        _('sex'),
        choices=[
            ('male', _('Male')),
            ('female', _('Female')),
        ],
        max_length=10,
    )
    birthday = models.DateField(
        _('Date of birth')
    )

    # Anthropometric data

    height = models.IntegerField(
        _('Height'),
        blank=True,
        null=True
    )
    weight = models.IntegerField(
        _('Weight'),
        blank=True,
        null=True
    )

    # Diagnostics

    is_diagnosed = models.BooleanField(
        _('was diagnosed'),
        default=False,
    )
    last_diagnostics = models.DateField(
        _('Last diagnostics'),
        null=True,
        default=None,
        blank=True
    )

    # Difficult exercises

    difficulty_level = models.CharField(
        _('Difficulty level'),
        choices=[
            ('beginner', _('Beginner')),
            ('normal', _('Normal')),
            ('hardcore', _('Hardcore')),
        ],
        default='beginner',
        max_length=10
    )

    @property
    def age(self) -> Optional[int]:
        if self.birthday is not None:
            date_now = datetime.date(datetime.now())
            result: timedelta = date_now - self.birthday
            return int(result.days / 365)
        return None

    @property
    def bmi(self) -> Optional[float]:
        """ИМТ применим для людей в диапазоне от 20 до 65 лет."""
        if self.age >= 20 and self.age <= 65:
            height_in_metrs = self.height / 100
            result = self.weight / (height_in_metrs ** 2)
            return round(result, 1)
        return None

    def __str__(self):
        if self.email:
            return self.email
        return self.username
