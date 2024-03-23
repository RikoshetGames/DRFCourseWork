from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from habits.models import NiceHabit
from habits.serializers.nice_habits import NiceHabitSerializer


class NiceHabitCreateAPIView(CreateAPIView):
    serializer_class = NiceHabitSerializer
    queryset = NiceHabit.objects.all()

    def perform_create(self, serializer):
        new_nice_habit = serializer.save()
        new_nice_habit.user = self.request.user
        new_nice_habit.save()


class NiceHabitListAPIView(ListAPIView):
    serializer_class = NiceHabitSerializer
    queryset = NiceHabit.objects.all()

    def get_queryset(self):
        user = self.request.user
        nice_habits_list = super().get_queryset()
        return nice_habits_list.filter(user=user)


class NiceHabitDetailAPIView(RetrieveAPIView):
    serializer_class = NiceHabitSerializer
    queryset = NiceHabit.objects.all()


class NiceHabitUpdateAPIView(UpdateAPIView):
    serializer_class = NiceHabitSerializer
    queryset = NiceHabit.objects.all()


class NiceHabitDeleteAPIView(DestroyAPIView):
    serializer_class = NiceHabitSerializer
    queryset = NiceHabit.objects.all()