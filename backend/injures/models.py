from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class BodyParts():
    NECK = 'neck'
    CHEST = 'chest'
    BACK = 'back'
    KNEES = 'knees'
    FEET = 'feet'
    HIPS = 'hips'
    SHOULDERS = 'shoulders'
    ELBOWS = 'elbows'
    BRUSHS = 'brushs'
    BODY_PARTS_LIST = (
        NECK, CHEST, BACK,
        KNEES, FEET, HIPS,
        SHOULDERS, ELBOWS, BRUSHS
    )
    BODY_PARTS_CHOISES = (
        (NECK, _('Neck')), (CHEST, _('Chest')), (BACK, _('BACK')),
        (KNEES, _('Knees')), (FEET, _('Feet')), (HIPS, _('Hips')),
        (SHOULDERS, _('Shoulders')), (ELBOWS, _('Elbows')),
        (BRUSHS, _('Brushs'))
    )


class Injure(models.Model):
    name = models.CharField(
        _('Имя болячки'),
        max_length=150
    )
    description = models.TextField(
        _('Description')
    )
    body_part = models.CharField(
        _('Body part'),
        choices=BodyParts.BODY_PARTS_CHOISES,
        max_length=10
    )

    def __str__(self):
        return self.name


class PersonalInjures(models.Model):
    DEGREE_OF_PAIN_CHOISES = (
        (0, _('Nothing')),
        (1, _('Little bit uncomfortable')),
        (2, _('Uncomfortable')),
        (3, _('Little ache')),
        (4, _('Pain')),
        (5, _('High pain')),
        (7, _('Painkillers - breakfast of champions')),
        (6, _('I cat`t do anything')),
        (8, _('I don`t move')),
        (9, _('I am the Pain!')),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='personal_injures',
        verbose_name=_('User')
    )
    injures = models.ForeignKey(
        Injure,
        on_delete=models.CASCADE,
        related_name='personal_injures',
        verbose_name=_('Injure'),
    )
    degree_of_pain = models.IntegerField(
        _('Degree of pain'),
        choices=DEGREE_OF_PAIN_CHOISES,
    )

    def __str__(self):
        return f'{self.user}:{self.injures.body_part} {self.degree_of_pain}'
