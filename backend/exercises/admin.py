from django.contrib import admin

from exercises.models import BaseExercisesModel
from injures.models import Injure, PersonalInjures
from users.models import User

admin.site.register(BaseExercisesModel)
admin.site.register(Injure)
admin.site.register(PersonalInjures)
