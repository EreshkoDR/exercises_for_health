# Generated by Django 4.1.7 on 2023-03-14 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Injure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя болячки')),
                ('description', models.TextField(verbose_name='Description')),
                ('body_part', models.CharField(choices=[('neck', 'Neck'), ('chest', 'Chest'), ('back', 'BACK'), ('knees', 'Knees'), ('feet', 'Feet'), ('hips', 'Hips'), ('shoulders', 'Shoulders'), ('elbows', 'Elbows'), ('brushs', 'Brushs')], max_length=10, verbose_name='Body part')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalInjures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree_of_pain', models.IntegerField(choices=[(0, 'Nothing'), (1, 'Little bit uncomfortable'), (2, 'Uncomfortable'), (3, 'Little ache'), (4, 'Pain'), (5, 'High pain'), (7, 'Painkillers - breakfast of champions'), (6, 'I cat`t do anything'), (8, 'I don`t move'), (9, 'I am the Pain!')], verbose_name='Degree of pain')),
                ('injures', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personal_injures', to='injures.injure', verbose_name='Injure')),
            ],
        ),
    ]