from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}

INTERVAL_CHOICES = [
    ('once_a_day', 'Один раз в день'),
    ('once_a_two_day', 'Один раз в два дня'),
    ('once_a_three_day', 'Один раз в три дня'),
    ('once_a_four_day', 'Один раз в четыре дня'),
    ('once_a_five_day', 'Один раз в пять дней'),
    ('once_a_six_day', 'Один раз в шесть дней'),
    ('once_a_seven_day', 'Один раз в семь дней'),
]


class NiceHabit(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    sign_nice_habit = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    action = models.CharField(max_length=100, verbose_name='Действие')

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Приятная привычка'
        verbose_name_plural = 'Приятные привычки'


class Habits(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Создатель привычки')
    place = models.CharField(max_length=100, verbose_name='Место выполнения')
    time = models.TimeField(verbose_name='Время начала выполнения')
    action = models.CharField(max_length=100, verbose_name='Действие')
    sign_nice_habit = models.BooleanField(default=False, verbose_name='Признак приятной привычки')
    associated_nice_habit = models.ForeignKey(NiceHabit, on_delete=models.SET_NULL, **NULLABLE,
                                              verbose_name='Связанная привычка', related_name='nice_habit')
    interval = models.CharField(max_length=100, verbose_name='Периодичность', choices=INTERVAL_CHOICES,
                                default='once_a_day')
    reward = models.CharField(max_length=200, **NULLABLE, verbose_name='Награда')
    duration_time = models.TimeField(verbose_name='Время выполнения')
    is_public = models.BooleanField(default=False, verbose_name='Публичная привычка')

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'