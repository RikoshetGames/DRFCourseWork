from rest_framework import serializers

from habits.models import Habits
from habits.serializers.nice_habits import NiceHabitSerializer


class HabitsSerializer(serializers.ModelSerializer):
    habits_count = serializers.SerializerMethodField()
    nice_habit = NiceHabitSerializer(many=True, read_only=True)

    def get_habits_count(self, obj):
        """Подсчет количества привычек"""
        return obj.habits.count()

    class Meta:
        model = Habits
        fields = '__all__'