from rest_framework import serializers

from habits.models import Habits
from habits.serializers.nice_habits import NiceHabitSerializer
from habits.validators import (TimeHabitsValidator, HabitsValidator, SignAssociatedNiceHabitsValidator,
                               IntervalHabitsValidator, SignNiceHabitsValidator)



class HabitsSerializer(serializers.ModelSerializer):
    # habits_count = serializers.SerializerMethodField()
    nice_habit = NiceHabitSerializer(many=True, read_only=True)
    validators = [TimeHabitsValidator('duration_time'), HabitsValidator(),
                  SignAssociatedNiceHabitsValidator('associated_nice_habit'), IntervalHabitsValidator('interval'),
                  SignNiceHabitsValidator()]

    # def get_habits_count(self, obj):
    #     """Подсчет количества привычек"""
    #     return obj.habits_set.count()

    class Meta:
        model = Habits
        fields = '__all__'