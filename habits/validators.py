from datetime import time

from rest_framework.exceptions import ValidationError


class HabitsValidator:
    """Проверяет наличие связанной привычки и награды"""

    def __call__(self, value):
        if value.get('associated_nice_habit') and value.get('reward'):
            raise ValidationError(
                'Можно выбрать только связанную приятную привычку или награду.')
        if not value.get('associated_nice_habit') and not value.get('reward'):
            raise ValidationError(
                'Нужно выбрать либо связанную приятную привычку, либо награду.')


class TimeHabitsValidator:
    """Проверяет время выполнения привычки"""

    max_time = time(0, 2, 0)

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        time = value.get(self.field)
        if time is not None and time > self.max_time:
            raise ValidationError('Превышено время выполнения привычки. Максимальное время - 2 минуты.')


class SignAssociatedNiceHabitsValidator:
    """Проверяет, является ли связанная привычка приятной привычкой"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        nice_habit = value.get(self.field)
        if nice_habit:
            if nice_habit.sign_nice_habit is False:
                raise ValidationError('Связанная привычка должна обладать признаком приятной привычки.')


INTERVAL_MAPPING = {
    'once_a_day': 1,
    'once_a_two_day': 2,
    'once_a_three_day': 3,
    'once_a_four_day': 4,
    'once_a_five_day': 5,
    'once_a_six_day': 6,
    'once_a_seven_day': 7,
}


class IntervalHabitsValidator:
    """Проверяет, не является ли периодичность реже, чем один раз в неделю"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        interval = value.get(self.field)
        interval_days = INTERVAL_MAPPING.get(interval, 0)
        if interval_days > 7:
            raise ValidationError('Периодичность выполнения привычки должна быть не реже одного раза в неделю.')


class SignNiceHabitsValidator:
    """Проверяет, является ли создаваемая привычка приятной привычкой"""

    def __call__(self, value):
        if value.get('sign_nice_habit'):
            if value.get('associated_nice_habit') or value.get('reward'):
                raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')
