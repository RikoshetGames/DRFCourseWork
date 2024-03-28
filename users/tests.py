from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    """Тестирование приятных"""

    def setUp(self):
        """Создание пользователя"""
        self.user = User.objects.create(
            name="test_user",
            email="test_user@test.com",
            password='987654321',
            telegram_id=None
        )

        # self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        """Тестирование создания пользователя"""

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('users:users_create'),
            {
                "name": "test_user2",
                "email": "test_user2@test.com",
                "password": "0987654321",
                "telegram_id": ""
            }
        )

        # print(response.json())

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_list_user(self):
        """Тестирование вывода списка пользователей"""

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('users:users_list')
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # print(response.json())

        self.assertEquals(
            response.json(),
            [
                {
                    "id": self.user.id,
                    "name": self.user.name,
                    "email": self.user.email,
                    "telegram_id": self.user.telegram_id
                }
            ]
        )

    def test_detail_user(self):
        """Тестирование вывода подробной информации о пользователе"""

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('users:users_detail', kwargs={'pk': self.user.id})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        # print(response.json())

        self.assertEquals(
            response.json(),

            {
                "id": self.user.id,
                "name": self.user.name,
                "email": self.user.email,
                "telegram_id": self.user.telegram_id

            }

        )

    def test_delete_user(self):
        """Тестирование удаления пользователя"""

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse('users:users_delete', kwargs={'pk': self.user.id})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_update_users(self):
        """Тестирование обновления приятной привычки"""

        updated_data = {
            "name": "test_user_33",
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            reverse('users:users_update', kwargs={'pk': self.user.id}),
            data=updated_data
        )

        # print(response.json())

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_user_not_owner(self):
        """Тестирование удаления пользователя, не являющегося владельцем учетной записи"""

        new_user = User.objects.create(
            name="test",
            email="test@test.ru",
            password="987654321",
            telegram_id="46464646"
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse('users:users_delete', kwargs={'pk': new_user.id})
        )

        # print(response.json())

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {'detail': 'Вы не являетесь владельцем этой учетной записи'}
        )

    def test_unauthorized__list_user(self):
        """Тестирование доступа к списку пользователей не авторизованному пользователю"""

        response = self.client.get(
            reverse('users:users_list')
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        # print(response.json())

        self.assertEqual(
            response.json(),
            {'detail': 'Учетные данные не были предоставлены.'}
        )
