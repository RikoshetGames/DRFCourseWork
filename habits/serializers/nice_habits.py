from rest_framework import serializers

from habits.models import NiceHabit


class NiceHabitSerializer(serializers.ModelSerializer):
    """Сериализатор приятных привычек для модели NiceHabits"""

    class Meta:
        model = NiceHabit
        fields = '__all__'