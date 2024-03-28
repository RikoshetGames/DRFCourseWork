from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habits, NiceHabit
from users.models import User


class HabitsTestCase(APITestCase):
    """Тестирование привычек"""

    def setUp(self):
        """ Создание пользователя и привычек """
        self.user = User.objects.create(
            name="test_user",
            email="test_user@test.com",
            password='987654321',
            telegram_id=None
        )
        self.nice_habit = NiceHabit.objects.create(
            owner=self.user,
            action="drink water",
            sign_nice_habit=True
        )
        self.habits = Habits.objects.create(
            owner=self.user,
            place="home",
            time="11:00:00",
            action="jumping",
            sign_nice_habit=False,
            associated_nice_habit=self.nice_habit,
            reward="",
            interval="once_a_three_day",
            is_public=False,
            duration_time="00:00:40",
        )

        self.client.force_authenticate(user=self.user)

    def test_create_habits(self):
        """Тестирование создания привычки"""

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('habits:habits_create'),
            {
                "owner": self.user.id,
                "place": "street",
                "time": "08:00:00",
                "action": "running",
                "sign_nice_habit": False,
                "associated_nice_habit": "",
                "reward": "drinking water",
                "interval": "once_a_two_day",
                "is_public": False,
                "duration_time": "00:01:40",
            }
        )

        # print(response.json())

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_list_habits(self):
        """Тестирование вывода списка привычек"""

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('habits:habits_list')
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # print(response.json())

        self.assertEquals(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.habits.id,
                        'place': self.habits.place,
                        'time': self.habits.time,
                        'action': self.habits.action,
                        'sign_nice_habit': self.habits.sign_nice_habit,
                        'interval': self.habits.interval,
                        'reward': self.habits.reward,
                        'duration_time': self.habits.duration_time,
                        'is_public': self.habits.is_public,
                        'owner': self.user.id,
                        'associated_nice_habit': self.nice_habit.id
                    }
                ]
            }
        )

    def test_detail_habits(self):
        """Тестирование получения привычки"""

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('habits:habits_detail', kwargs={'pk': self.habits.id})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # print(response.json())

        self.assertEquals(
            response.json(),
            {
                'id': self.habits.id,
                'place': self.habits.place,
                'time': self.habits.time,
                'action': self.habits.action,
                'sign_nice_habit': self.habits.sign_nice_habit,
                'interval': self.habits.interval,
                'reward': self.habits.reward,
                'duration_time': self.habits.duration_time,
                'is_public': self.habits.is_public,
                'owner': self.user.id,
                'associated_nice_habit': self.nice_habit.id
            }
        )

    def test_delete_habits(self):
        """Тестирование удаления привычки"""

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse('habits:habits_delete', kwargs={'pk': self.habits.id})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_update_habits(self):
        """Тестирование обновления привычки"""

        updated_data = {
            "action": "swimming",
            "associated_nice_habit": "",
            "reward": "ice cream",
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            reverse('habits:habits_update', kwargs={'pk': self.habits.id}),
            data=updated_data
        )

        # print(response.json())

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_create_not_valid_habits(self):
        """Тестирование невалидного создания привычки"""

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('habits:habits_create'),
            {
                "owner": self.user.id,
                "place": "street",
                "time": "08:00:00",
                "action": "running",
                "sign_nice_habit": False,
                "associated_nice_habit": "",
                "reward": "drinking water",
                "interval": "once_a_two_day",
                "is_public": False,
                "duration_time": "00:02:40",
            }
        )

        # print(response.json())

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Превышено время выполнения привычки. Максимальное время - 2 минуты.']}
        )

    def test_create_not_valid_habits_2(self):
        """Тестирование невалидного создания привычки"""

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('habits:habits_create'),
            {
                "owner": self.user.id,
                "place": "street",
                "time": "08:00:00",
                "action": "running",
                "sign_nice_habit": False,
                "associated_nice_habit": "",
                "reward": "",
                "interval": "once_a_two_day",
                "is_public": False,
                "duration_time": "00:01:40",
            }
        )

        # print(response.json())

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Нужно выбрать либо связанную приятную привычку, либо награду.']}
        )

    def test_create_not_valid_habits_3(self):
        """Тестирование невалидного создания привычки"""

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('habits:habits_create'),
            {
                "owner": self.user.id,
                "place": "street",
                "time": "08:00:00",
                "action": "running",
                "sign_nice_habit": False,
                "associated_nice_habit": self.nice_habit.id,
                "reward": "water_bottle",
                "interval": "once_a_two_day",
                "is_public": False,
                "duration_time": "00:01:40",
            }
        )

        # print(response.json())

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Можно выбрать только связанную приятную привычку или награду.']}
        )

    def test_create_not_valid_habits_4(self):
        """Тестирование невалидного создания привычки"""

        self.client.force_authenticate(user=self.user)

        self.new_nice_habit = NiceHabit.objects.create(
            owner=self.user,
            action="drink water",
            sign_nice_habit=False
        )

        response = self.client.post(
            reverse('habits:habits_create'),
            {
                "owner": self.user.id,
                "place": "street",
                "time": "08:00:00",
                "action": "running",
                "sign_nice_habit": False,
                "associated_nice_habit": self.new_nice_habit.id,
                "reward": "",
                "interval": "once_a_two_day",
                "is_public": False,
                "duration_time": "00:01:40",
            }
        )

        # print(response.json())

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Связанная привычка должна обладать признаком приятной привычки.']}
        )

    def test_create_not_valid_habits_5(self):
        """Тестирование невалидного создания привычки"""

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('habits:habits_create'),
            {
                "owner": self.user.id,
                "place": "street",
                "time": "08:00:00",
                "action": "running",
                "sign_nice_habit": True,
                "associated_nice_habit": "",
                "reward": "water_bottle",
                "interval": "once_a_two_day",
                "is_public": False,
                "duration_time": "00:01:40",
            }
        )

        # print(response.json())

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['У приятной привычки не может быть вознаграждения или связанной привычки.']}
        )


class NiceHabitsTestCase(APITestCase):
    """Тестирование приятных привычек"""

    def setUp(self):
        """ Создание пользователя и приятной привычки """
        self.user = User.objects.create(
            name="test_user",
            email="test_user@test.com",
            password='987654321',
            telegram_id=None
        )
        self.nice_habit = NiceHabit.objects.create(
            owner=self.user,
            action="drink water",
            sign_nice_habit=True
        )

        self.client.force_authenticate(user=self.user)

    def test_create_nice_habits(self):
        """Тестирование создания приятной привычки"""

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('habits:nice_habits_create'),
            {
                "owner": self.user.id,
                "sign_nice_habit": True,
                "action": "Отдохнуть",
            }
        )

        # print(response.json())

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_list_nice_habits(self):
        """Тестирование вывода списка приятных привычек"""

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('habits:nice_habits_list')
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # print(response.json())

        self.assertEquals(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'owner': self.user.id,
                        'id': self.nice_habit.id,
                        'action': self.nice_habit.action,
                        'sign_nice_habit': self.nice_habit.sign_nice_habit,
                    }
                ]
            }
        )

    def test_detail_nice_habits(self):
        """Тестирование получения приятных привычки"""

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('habits:nice_habits_detail', kwargs={'pk': self.nice_habit.id})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # print(response.json())

        self.assertEquals(
            response.json(),
            {
                'owner': self.user.id,
                'id': self.nice_habit.id,
                'action': self.nice_habit.action,
                'sign_nice_habit': self.nice_habit.sign_nice_habit,
            }
        )

    def test_delete_nice_habits(self):
        """Тестирование удаления приятной привычки"""

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse('habits:nice_habits_delete', kwargs={'pk': self.nice_habit.id})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_update_habits(self):
        """Тестирование обновления приятной привычки"""

        updated_data = {
            "sign_nice_habit": False,
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            reverse('habits:nice_habits_update', kwargs={'pk': self.nice_habit.id}),
            data=updated_data
        )

        # print(response.json())

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )
