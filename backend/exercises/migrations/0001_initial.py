# Generated by Django 4.1.7 on 2023-03-14 11:05

import pathlib

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseExercisesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name of exercise')),
                ('body_part', models.CharField(choices=[('neck', 'Neck'), ('chest', 'Chest'), ('back', 'BACK'), ('knees', 'Knees'), ('feet', 'Feet'), ('hips', 'Hips'), ('shoulders', 'Shoulders'), ('elbows', 'Elbows'), ('brushs', 'Brushs')], max_length=10, verbose_name='Part of body')),
                ('difficulty', models.CharField(choices=[('beginner', 'Beginner'), ('normal', 'Normal'), ('hardcore', 'Hardcore')], max_length=10, verbose_name='Difficulty of exercise')),
                ('type_of_activity', models.CharField(choices=[('power', 'Power'), ('stretch', 'Stretch'), ('mix', 'Mix'), ('static', 'Static'), ('warm_up', 'Warm up'), ('warm_down', 'Warm down')], max_length=10, verbose_name='Type of activity')),
                ('description', models.TextField(verbose_name='Descriptoin of exercise')),
                ('exercise', models.TextField(verbose_name='Description for doing exercise')),
                ('file', models.FileField(upload_to=pathlib.PureWindowsPath('D:/dev/projects/pet/backend_kinezis/backend/media/exercises/<django.db.models.fields.CharField>'))),
            ],
        ),
    ]
