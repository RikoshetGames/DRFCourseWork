from django.urls import path

from habits.apps import HabitsConfig
from habits.views.habits import HabitListAPIView, HabitDetailAPIView, HabitCreateAPIView, HabitUpdateAPIView, \
    HabitDeleteAPIView, HabitPublicListAPIView

from habits.views.nice_habits import NiceHabitListAPIView, NiceHabitDetailAPIView, NiceHabitCreateAPIView, \
    NiceHabitUpdateAPIView, NiceHabitDeleteAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('habits/', HabitListAPIView.as_view(), name='habits_list'),
    path('habits/<int:pk>/', HabitDetailAPIView.as_view(), name='habits_detail'),
    path('habits/create/', HabitCreateAPIView.as_view(), name='habits_create'),
    path('habits/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habits_update'),
    path('habits/delete/<int:pk>/', HabitDeleteAPIView.as_view(), name='habits_delete'),

    path('public_habits/', HabitPublicListAPIView.as_view(), name='public_habits_list'),

    path('nice_habits/', NiceHabitListAPIView.as_view(), name='nice_habits_list'),
    path('nice_habits/<int:pk>/', NiceHabitDetailAPIView.as_view(), name='nice_habits_detail'),
    path('nice_habits/create/', NiceHabitCreateAPIView.as_view(), name='nice_habits_create'),
    path('nice_habits/update/<int:pk>/', NiceHabitUpdateAPIView.as_view(), name='nice_habits_update'),
    path('nice_habits/delete/<int:pk>/', NiceHabitDeleteAPIView.as_view(), name='nice_habits_delete'),
]