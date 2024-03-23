from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from habits.models import Habits
from habits.serializers.habits import HabitsSerializer


class HabitCreateAPIView(CreateAPIView):
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()


class HabitListAPIView(ListAPIView):
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()

    def get_queryset(self):
        user = self.request.user
        habits_list = super().get_queryset()
        return habits_list.filter(user=user)


class HabitDetailAPIView(RetrieveAPIView):
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()


class HabitUpdateAPIView(UpdateAPIView):
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()


class HabitDeleteAPIView(DestroyAPIView):
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()


class HabitPublicListAPIView(ListAPIView):
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all().filter(is_public=True)